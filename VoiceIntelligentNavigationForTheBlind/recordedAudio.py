import webrtcvad
import collections
import sys
import signal
import pyaudio
from array import array
from struct import pack
import wave
import time
import os
from pydub import AudioSegment  # 导入pydub库用于音频格式转换

# 音频格式，这里设置为16位整数
FORMAT = pyaudio.paInt16
# 声道数，设置为单声道（1）
CHANNELS = 1
# 采样率，设置为16000Hz
RATE = 16000
# 每个音频数据块的持续时间（单位：毫秒），支持10、20和30毫秒，这里设置为30毫秒
CHUNK_DURATION_MS = 30  
# 用于判断语音起止的额外缓冲时长（单位：毫秒），这里设置为1500毫秒（即1.5秒）
PADDING_DURATION_MS = 1500  
# 根据采样率和数据块持续时间计算出每个数据块的采样点数
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  
# 每个数据块的字节数，因为是16位（2字节）的PCM数据，所以乘以2
CHUNK_BYTES = CHUNK_SIZE * 2  
# 根据缓冲时长和数据块持续时间计算出缓冲数据块的数量
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
# 用于起始检测的窗口包含的数据块数量（以400毫秒窗口时长和数据块持续时间计算）
NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  
# 用于结束检测的窗口包含的数据块数量（是起始检测窗口数据块数量的2倍）
NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2

# 起始偏移量，用于在音频数据中定位合适的起始点，根据相关参数计算得出
START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)


# 函数功能：将从麦克风录制的数据保存到指定路径的文件中
# 参数：
# - path：要保存的文件路径
# - data：音频数据（以数组形式表示）
# - sample_width：样本宽度（字节数）
def record_to_file(path, data, sample_width):
    """Records from the microphone and outputs the resulting data to 'path'"""
    # 将音频数据按照小端序（<）和对应格式（'h'表示16位整数，对应数据中的每个元素格式）进行打包
    data = pack('<' + ('h' * len(data)), *data)
    # 以写入二进制模式打开WAV文件
    wf = wave.open(path, 'wb')
    # 设置声道数为1
    wf.setnchannels(1)
    # 设置样本宽度（字节数）
    wf.setsampwidth(sample_width)
    # 设置采样率
    wf.setframerate(RATE)
    # 将打包好的音频数据写入文件
    wf.writeframes(data)
    # 关闭文件
    wf.close()


# 函数功能：对音频数据进行音量归一化处理，使音量平均化
# 参数：
# - snd_data：音频数据数组
def normalize(snd_data):
    """Average the volume out"""
    # 16位整数能表示的最大值，用于归一化计算的参考值
    MAXIMUM = 32767  
    # 计算归一化的缩放因子，用最大值除以音频数据中绝对值的最大值
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)
    r = array('h')
    # 遍历音频数据，对每个元素进行缩放并添加到新的数组中
    for i in snd_data:
        r.append(int(i * times))
    return r

#录制音频并转成MP3格式
def record_audio():
    # 创建一个VAD（Voice Activity Detection，语音活动检测）对象，参数2表示中等严格程度的检测模式
        vad = webrtcvad.Vad(2)

        # 创建一个PyAudio对象，用于音频相关操作
        pa = pyaudio.PyAudio()
        # 打开音频输入流，配置相关参数
        stream = pa.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         start=False,
                         # input_device_index=2,  # 如果需要指定特定的输入设备，可以取消注释并设置正确的设备索引
                         frames_per_buffer=CHUNK_SIZE)

        # 标记是否检测到一个语音片段，初始化为False
        got_a_sentence = False
        # 标记是否结束当前录制循环，初始化为False
        leave = False

        # 内层循环，用于一次语音录制的具体操作
        while not leave:
            # 创建一个双端队列作为环形缓冲区，用于存储音频数据块，设置最大长度为缓冲数据块数量
            ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
            # 标记是否触发语音开始检测，初始化为False
            triggered = False
            # 用于存储检测到的有语音的音频数据块
            voiced_frames = []
            # 用于记录起始检测窗口内每个数据块是否有语音的标志数组，初始化为全0
            ring_buffer_flags = [0] * NUM_WINDOW_CHUNKS
            # 起始检测窗口内当前处理的数据块索引，初始化为0
            ring_buffer_index = 0

            # 用于记录结束检测窗口内每个数据块是否有语音的标志数组，初始化为全0
            ring_buffer_flags_end = [0] * NUM_WINDOW_CHUNKS_END
            # 结束检测窗口内当前处理的数据块索引，初始化为0
            ring_buffer_index_end = 0
            # 用于临时存储音频数据的字符串，初始为空
            buffer_in = ''
            # WangS，创建一个数组用于存储原始音频数据（以16位整数形式）
            raw_data = array('h')
            index = 0
            start_point = 0
            StartTime = time.time()
            print("* recording: ")
            # 启动音频输入流，开始读取音频数据
            stream.start_stream()

            # 循环读取音频数据，直到检测到一个语音片段或者满足结束条件
            while not got_a_sentence and not leave:
                # 从音频流中读取一个数据块大小的数据，设置异常处理模式（这里不抛出缓冲区溢出异常）
                chunk = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                # WangS，将读取到的数据块添加到原始音频数据数组中
                raw_data.extend(array('h', chunk))
                index += CHUNK_SIZE
                # 使用VAD检测当前数据块是否包含语音，传入数据块和采样率
                active = vad.is_speech(chunk, RATE)

                # sys.stdout.write('1' if active else '_')  # 可以用于输出当前数据块是否有语音的可视化表示，这里注释掉了
                # 将当前数据块的语音标志存入起始检测窗口标志数组中
                ring_buffer_flags[ring_buffer_index] = 1 if active else 0
                # 更新起始检测窗口内的数据块索引，实现环形缓冲区的效果
                ring_buffer_index += 1
                ring_buffer_index %= NUM_WINDOW_CHUNKS

                # 将当前数据块的语音标志存入结束检测窗口标志数组中
                ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
                # 更新结束检测窗口内的数据块索引，实现环形缓冲区的效果
                ring_buffer_index_end += 1
                ring_buffer_index_end %= NUM_WINDOW_CHUNKS_END

                # 语音起始点检测逻辑
                if not triggered:
                    # 将当前数据块添加到环形缓冲区中
                    ring_buffer.append(chunk)
                    # 统计起始检测窗口内有语音的数据块数量
                    num_voiced = sum(ring_buffer_flags)
                    # 如果有语音的数据块数量超过一定比例（这里是窗口数据块数量的80%），则认为语音开始了
                    if num_voiced > 0.8 * NUM_WINDOW_CHUNKS:
                        sys.stdout.write(' Open ')
                        StartTime = time.time()
                        triggered = True
                        # 记录语音起始点对应的音频数据索引位置，做一定的偏移调整
                        start_point = index - CHUNK_SIZE * 20  
                        # voiced_frames.extend(ring_buffer)  # 可以将环形缓冲区的数据添加到有语音数据块列表中，这里注释掉了
                        ring_buffer.clear()
                # 语音结束点检测逻辑
                else:
                    # voiced_frames.append(chunk)  # 可以将当前数据块添加到有语音数据块列表中，这里注释掉了
                    ring_buffer.append(chunk)
                    # 统计结束检测窗口内无语音的数据块数量
                    num_unvoiced = NUM_WINDOW_CHUNKS_END - sum(ring_buffer_flags_end)
                    # 如果无语音的数据块数量超过一定比例（这里是窗口数据块数量的90%），或者录制时间超过10秒，则认为语音结束了
                    if num_unvoiced > 0.90 * NUM_WINDOW_CHUNKS_END or (time.time() - StartTime) > 10:
                        sys.stdout.write(' Close ')
                        triggered = False
                        got_a_sentence = True

                sys.stdout.flush()

            sys.stdout.write('\n')
            # data = b''.join(voiced_frames)  # 可以将有语音的数据块拼接起来，这里注释掉了

            # 停止音频输入流
            stream.stop_stream()
            print("* done recording")
            got_a_sentence = False

            # 将原始音频数据反转，方便后续处理起始点相关操作
            raw_data.reverse()
            # 根据起始点索引，删除起始点之前的音频数据
            for index in range(start_point):
                raw_data.pop()
            # 再将音频数据反转回来，恢复正常顺序
            raw_data.reverse()
            # 对音频数据进行音量归一化处理
            raw_data = normalize(raw_data)
            # 先保存为WAV文件（后续将基于此WAV文件转换为MP3）
            record_to_file("record.wav", raw_data, 2)

            # 使用pydub库将WAV文件转换为MP3文件
            sound = AudioSegment.from_wav("record.wav")
            sound.export("record.mp3", format="mp3")

            leave = True

        # 关闭音频输入流
        stream.close()
        # 使用系统命令调用音频播放工具播放录制好的MP3文件（需确保系统有相应音频播放命令可用，如play命令对MP3格式支持）
        os.system("play record.mp3")


if __name__ == '__main__':
    record_audio()