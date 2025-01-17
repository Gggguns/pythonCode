# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: heartbeat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fheartbeat.proto\"a\n\x10HeartbeatRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x10\n\x08latitude\x18\x02 \x01(\x01\x12\x11\n\tlongitude\x18\x03 \x01(\x01\x12\x15\n\rrandom_number\x18\x04 \x01(\x05\"#\n\x11HeartbeatResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\"*\n\x15\x43lientLocationRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\"9\n\x16\x43lientLocationResponse\x12\x1f\n\x07\x63lients\x18\x01 \x03(\x0b\x32\x0e.NearestClient\"K\n\rNearestClient\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x15\n\rrandom_number\x18\x02 \x01(\x05\x12\x10\n\x08\x64istance\x18\x03 \x01(\x01\x32\x8c\x01\n\x10HeartbeatService\x12\x32\n\tHeartbeat\x12\x11.HeartbeatRequest\x1a\x12.HeartbeatResponse\x12\x44\n\x11GetNearestClients\x12\x16.ClientLocationRequest\x1a\x17.ClientLocationResponseb\x06proto3')



_HEARTBEATREQUEST = DESCRIPTOR.message_types_by_name['HeartbeatRequest']
_HEARTBEATRESPONSE = DESCRIPTOR.message_types_by_name['HeartbeatResponse']
_CLIENTLOCATIONREQUEST = DESCRIPTOR.message_types_by_name['ClientLocationRequest']
_CLIENTLOCATIONRESPONSE = DESCRIPTOR.message_types_by_name['ClientLocationResponse']
_NEARESTCLIENT = DESCRIPTOR.message_types_by_name['NearestClient']
HeartbeatRequest = _reflection.GeneratedProtocolMessageType('HeartbeatRequest', (_message.Message,), {
  'DESCRIPTOR' : _HEARTBEATREQUEST,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:HeartbeatRequest)
  })
_sym_db.RegisterMessage(HeartbeatRequest)

HeartbeatResponse = _reflection.GeneratedProtocolMessageType('HeartbeatResponse', (_message.Message,), {
  'DESCRIPTOR' : _HEARTBEATRESPONSE,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:HeartbeatResponse)
  })
_sym_db.RegisterMessage(HeartbeatResponse)

ClientLocationRequest = _reflection.GeneratedProtocolMessageType('ClientLocationRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTLOCATIONREQUEST,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:ClientLocationRequest)
  })
_sym_db.RegisterMessage(ClientLocationRequest)

ClientLocationResponse = _reflection.GeneratedProtocolMessageType('ClientLocationResponse', (_message.Message,), {
  'DESCRIPTOR' : _CLIENTLOCATIONRESPONSE,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:ClientLocationResponse)
  })
_sym_db.RegisterMessage(ClientLocationResponse)

NearestClient = _reflection.GeneratedProtocolMessageType('NearestClient', (_message.Message,), {
  'DESCRIPTOR' : _NEARESTCLIENT,
  '__module__' : 'heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:NearestClient)
  })
_sym_db.RegisterMessage(NearestClient)

_HEARTBEATSERVICE = DESCRIPTOR.services_by_name['HeartbeatService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _HEARTBEATREQUEST._serialized_start=19
  _HEARTBEATREQUEST._serialized_end=116
  _HEARTBEATRESPONSE._serialized_start=118
  _HEARTBEATRESPONSE._serialized_end=153
  _CLIENTLOCATIONREQUEST._serialized_start=155
  _CLIENTLOCATIONREQUEST._serialized_end=197
  _CLIENTLOCATIONRESPONSE._serialized_start=199
  _CLIENTLOCATIONRESPONSE._serialized_end=256
  _NEARESTCLIENT._serialized_start=258
  _NEARESTCLIENT._serialized_end=333
  _HEARTBEATSERVICE._serialized_start=336
  _HEARTBEATSERVICE._serialized_end=476
# @@protoc_insertion_point(module_scope)
