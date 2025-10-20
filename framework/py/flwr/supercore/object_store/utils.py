# Copyright 2025 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Utils for ObjectStore."""


from typing import Union

from flwr.proto.appio_pb2 import PushAppMessagesRequest  # pylint: disable=E0611
from flwr.proto.fleet_pb2 import PushMessagesRequest  # pylint: disable=E0611

from . import ObjectStore


def store_mapping_and_register_objects(
    store: ObjectStore, request: Union[PushAppMessagesRequest, PushMessagesRequest]
) -> set[str]:
    """Store Message object to descendants mapping and preregister objects."""
    messages_list = request.messages_list
    if not messages_list:
        return set()
    objects_to_push: set[str] = set()
    run_id = messages_list[0].metadata.run_id
    preregister = store.preregister
    message_object_trees = request.message_object_trees

    for object_tree in message_object_trees:
        unavailable_obj_ids = preregister(run_id, object_tree)
        objects_to_push.update(unavailable_obj_ids)

    return objects_to_push
