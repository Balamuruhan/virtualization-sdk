#
# Copyright (c) 2019 by Delphix. All rights reserved.
#

import enum
from dlpx.virtualization import common_pb2
from dlpx.virtualization.platform.exceptions import IncorrectTypeError

"""Classes used for Plugin Operations

This module defines the non autogenerated classes used as input/output for
plugin operations. These are used instead of protobuf generated classes to
hide the implemenatation details for protobufs and also to provide the
correct types. For example, protobufs store the plugin defined properties
as json. However the plugin operations get these properties as an instance
of the autogenerated classes from the schemas (e.g. VirtualSourceDefinition)
"""

__all__ = [
    "VirtualSource",
    "StagedSource",
    "DirectSource",
    "RemoteConnection",
    "Status",
    "Mount",
    "OwnershipSpecification",
    "MountSpecification"]


class VirtualSource(object):

    def __init__(self, guid, connection, parameters, mounts):
        self._guid = guid
        self._connection = connection
        self._parameters = parameters
        self._mounts = mounts

    @property
    def guid(self):
        """str: The unique guid identifier of this VirtualSource."""
        return self._guid

    @property
    def connection(self):
        """RemoteConnection: The RemoteConnection for this VirtualSource."""
        return self._connection

    @property
    def parameters(self):
        """VirtualSourceDefinition: The parameters of this VirtualSource."""
        return self._parameters

    @property
    def mounts(self):
        """list(Mount): The mounts of this VirtualSource."""
        return self._mounts


class StagedSource(object):

    def __init__(self, guid, source_connection, parameters, mount, staged_connection):
        self._guid = guid
        self._source_connection = source_connection
        self._parameters = parameters
        self._mount = mount
        self._staged_connection = staged_connection

    @property
    def guid(self):
        """str: The unique guid identifier for this StagedSource."""
        return self._guid

    @property
    def source_connection(self):
        """SourceConnection: The RemoteConnection representing the source
        environment for this StagedSource."""
        return self._source_connection

    @property
    def parameters(self):
        """LinkedSourceDefinition: The LinkedSourceDefinition for this
        StagedSource.
        """
        return self._parameters

    @property
    def mount(self):
        """MountSpecification: The MountSpecification for this StagedSource."""
        return self._mount

    @property
    def staged_connection(self):
        """StagedConnection: The RemoteConnection representing the staging
        environment for this StagedSource."""
        return self._staged_connection


class DirectSource(object):

    def __init__(self, guid, connection, parameters):
        self._guid = guid
        self._connection = connection
        self._parameters = parameters

    @property
    def guid(self):
        """str: The unique guid identifier for this DirectSource."""
        return self._guid

    @property
    def connection(self):
        """RemoteConnection: The RemoteConnection for this DirectSource."""
        return self._connection

    @property
    def parameters(self):
        """LinkedSourceDefinition: The LinkedSourceDefinition for this
        DirectSource.
        """
        return self._parameters


class RemoteConnection(object):

    def __init__(self, environment, user):
        self._environment = environment
        self._user = user

    @property
    def environment(self):
        """RemoteEnvironment: The RemoteEnvironment for this RemoteConnection.
        """
        return self._environment

    @property
    def user(self):
        """RemoteUser: The RemoteUser for this RemoteConnection."""
        return self._user


class Status(enum.Enum):
    ACTIVE = 0
    INACTIVE = 1

#
# Only the next 3 classes need to have validation as the plugin writer actually
# creates objects of these types unlike any other defined classes.
#


class Mount(object):
    def __init__(self, remote_environment, mount_path, shared_path=None):
        if not isinstance(remote_environment, common_pb2.RemoteEnvironment):
            raise IncorrectTypeError(
                Mount,
                'remote_environment',
                type(remote_environment),
                common_pb2.RemoteEnvironment)
        self._remote_environment = remote_environment

        if not isinstance(mount_path, basestring):
            raise IncorrectTypeError(
                Mount, 'mount_path', type(mount_path), basestring)
        self._mount_path = mount_path

        if shared_path and not isinstance(shared_path, basestring):
            raise IncorrectTypeError(
                Mount, 'shared_path', type(shared_path), basestring, False)
        self._shared_path = shared_path

    @property
    def remote_environment(self):
        """RemoteEnvironment: The RemoteEnvironment for this Mount."""
        return self._remote_environment

    @property
    def mount_path(self):
        """str: The path on the environment to mount to for this Mount."""
        return self._mount_path

    @property
    def shared_path(self):
        """str: The subset of the ZFS filesystem to mount on the mount_path."""
        return self._shared_path


class OwnershipSpecification(object):
    def __init__(self, uid, gid):
        if not isinstance(uid, int):
            raise IncorrectTypeError(
                OwnershipSpecification, 'uid', type(uid), int)
        self._uid = uid
        if not isinstance(gid, int):
            raise IncorrectTypeError(
                OwnershipSpecification, 'gid', type(gid), int)
        self._gid = gid

    @property
    def uid(self):
        """int: The user id for this OwnershipSpecification."""
        return self._uid

    @property
    def gid(self):
        """int: The group id for this OwnershipSpecification."""
        return self._gid


class MountSpecification(object):
    def __init__(self, mounts, ownership_specification=None):
        if not isinstance(mounts, list):
            raise IncorrectTypeError(
                MountSpecification, 'mounts', type(mounts), [Mount])
        if not all(isinstance(mount, Mount) for mount in mounts):
            raise IncorrectTypeError(
                MountSpecification,
                'mounts',
                [type(mount) for mount in mounts],
                [Mount])
        self._mounts = mounts

        if (ownership_specification and not isinstance(
                ownership_specification, OwnershipSpecification)):
            raise IncorrectTypeError(
                MountSpecification,
                'ownership_specification',
                type(ownership_specification),
                OwnershipSpecification,
                False)

        self._ownership_specification = ownership_specification

    @property
    def mounts(self):
        """list of Mount: List of mounts for this MountSpecification"""
        return self._mounts

    @property
    def ownership_specification(self):
        """OwnershipSpecification: The OwnershipSpecification for this
        MountSpecification.
        """
        return self._ownership_specification
