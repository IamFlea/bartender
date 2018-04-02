#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" pymemory.py: process memory management functions and class by Flea 

Usage:  

import pymemory.pymemory as pm 
pm.load_process("notepad.exe")
with pm:
    integer = pm.uint32(pm.base_address)
    print(hex(integer))

TODO
    1) get information if the process is 64 bit or 32bit (AoK HD.exe should be always 32bit anyway)
""" 
import sys
import re 
import os

from ctypes import *
from ctypes.wintypes import *
from struct import unpack, calcsize
from math import ceil as roundup # Not chemical glyphosate... but mathematical roundup. 

def print_addr(integer):
    """ For debugging porposes - prints the address. """
    stuff = "" if integer < 2**32 else " Warning: out of 32-bit space!"
    stuff = stuff if integer >= 0 else " Warning: this is not an address."
    print("Address: "+hex(integer) + "" + stuff)
  
class NullAddress(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PyMemory(object):
    """This class serves for memory management. """
    PROCESS_ALL_ACCESS = 0x1F0FFF
    BUFFER_SIZE = 0x10000 # 65 kb seems big enough

    def __init__(self):
        """ Does nothing """
        super(PyMemory, self).__init__()
        # Variables used in getting Base address
        self.pid = None
        self.access = None
        self.process_name = None
        self.module_name = None
        # Variables used in reading process memory
        self.base_address = None
        self.process_handle = None
        self.fmt_size_lookup = None
        self.memory_regions = None
        self.buffer = create_string_buffer(PyMemory.BUFFER_SIZE)

    def __get_pid__(process_name):
        """ Returns `PID` from the process name. """
        #PSAPI.DLL
        psapi = windll.psapi
        #Kernel32.DLL
        kernel = windll.kernel32

        arr = c_ulong * 256
        lpidProcess= arr()
        cb = sizeof(lpidProcess)
        cbNeeded = c_ulong()
        hModule = c_ulong()
        count = c_ulong()
        modname = c_buffer(64)
        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010
        #Call Enumprocesses to get hold of process id's
        psapi.EnumProcesses(byref(lpidProcess), cb, byref(cbNeeded))
        #Number of processes returned
        nReturned = cbNeeded.value//sizeof(c_ulong())
        pidProcess = [i for i in lpidProcess][:nReturned]
        for pid in pidProcess:
            #Get handle to the process based on PID
            hProcess = kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
            if hProcess:
                psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
                psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, sizeof(modname))
                name = modname.raw.split(b"\x00")[0].decode("utf-8")
                modname = c_buffer(64)
                if name == process_name:
                    return pid
                kernel.CloseHandle(hProcess)
        raise ProcessLookupError(f"Couldn't get PID of `{process_name}`.")

    def __get_base_address__(self, module_name):
        """ Returns `base address` from the pid"""
        # const variable
        TH32CS_SNAPMODULE = 0x00000008
        
        class MODULEENTRY32(Structure):
            _fields_ = [('dwSize', DWORD), 
                        ('th32ModuleID', DWORD), 
                        ('th32ProcessID', DWORD),
                        ('GlblcntUsage', DWORD),
                        ('ProccntUsage', DWORD),
                        ('modBaseAddr', POINTER(BYTE)),
                        ('modBaseSize', DWORD), 
                        ('hModule', HMODULE),
                        ('szModule', c_char * 256),
                        ('szExePath', c_char * 260)]
        
        me32 = MODULEENTRY32()
        me32.dwSize = sizeof(MODULEENTRY32)
        hModuleSnap = windll.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, self.pid)
        ret = windll.kernel32.Module32First(hModuleSnap, pointer(me32))
        while ret:
            if me32.szModule == str.encode(module_name):
                result = addressof(me32.modBaseAddr.contents)
                windll.kernel32.CloseHandle(hModuleSnap)
                return result
            ret = windll.kernel32.Module32Next(hModuleSnap, pointer(me32))
        windll.kernel32.CloseHandle(hModuleSnap)
        raise ProcessLookupError(f"Process `{process_name}` not found.")
        
    def load_process(self, process_name, module_name=None, access=None):
        """ Loads PID and base address and set access"""
        if module_name is None:
            module_name = process_name 
        # Get PID and base adress
        self.pid = PyMemory.__get_pid__(process_name)
        self.base_address = self.__get_base_address__(module_name)
        self.access = access if access else PyMemory.PROCESS_ALL_ACCESS
        self.process_name = process_name
        self.module_name = module_name

    def __enter__(self):
        """ Open process handler """ 
        self.process_handle = windll.kernel32.OpenProcess(self.access, False, self.pid)
        self.update()
        return self

    def __exit__(self, type, value, traceback):
        """ Closes process handler """ 
        windll.kernel32.CloseHandle(self.process_handle)

    def buffer_load(self, address, size):
        # Care, size is in BYTES
        windll.kernel32.ReadProcessMemory(self.process_handle, address, self.buffer, size, byref(c_size_t(0)))

    def pointer(self, address):
        self.buffer_load(address, 4)
        address = unpack("I", self.buffer[:4])[0] 
        for start, end in self.memory_regions:
            if address < end and address > start:
                return address
        raise NullAddress(address)

    def int8(self, address):
        self.buffer_load(address, 1)
        return unpack("b", self.buffer[:1])[0] 

    def uint8(self, address):
        self.buffer_load(address, 1)
        return unpack("b", self.buffer[:1])[0] 

    def int16(self, address):
        self.buffer_load(address, 2)
        return unpack("h", self.buffer[:2])[0] 

    def uint16(self, address):
        self.buffer_load(address, 2)
        return unpack("H", self.buffer[:2])[0] 

    def int32(self, address):
        self.buffer_load(address, 4)
        return unpack("i", self.buffer[:4])[0] 

    def uint32(self, address):
        self.buffer_load(address, 4)
        return unpack("I", self.buffer[:4])[0] 

    def int64(self, address):
        self.buffer_load(address, 8)
        return unpack("q", self.buffer[:8])[0] 

    def uint64(self, address):
        self.buffer_load(address, 8)
        return unpack("Q", self.buffer[:8])[0] 

    def float(self, address):
        self.buffer_load(address, 4)
        return unpack("f", self.buffer[:4])[0] 

    def double(self, address):
        self.buffer_load(address, 8)
        return unpack("d", self.buffer[:8])[0] 

    def string(self, address, length=32):
        self.buffer_load(address, length)
        result = unpack(f"{length}s", self.buffer[:length])[0]
        if result[0] == b"\x00":
            return ""
        return result.split(b"\x00")[0].decode("utf-8")

    def byte_string(self, address, length=32):
        self.buffer_load(address, length)
        return self.buffer[:length].split(b"\x00")[0]

    def struct(self, address, fmt):
        size = calcsize(fmt)
        result = []
        for _ in range(roundup(size/PyMemory.BUFFER_SIZE)):
            self.buffer_load(address, size)
            result += unpack(fmt, self.buffer[:size])
        return result

    def buff_pointer(self, offset):
        address = unpack("I", self.buffer[offset:offset+4])[0] 
        if address:
            return address
        else:
            raise NullAddress(address)

    def buff_int8(self, offset):
        return unpack("b", self.buffer[offset:offset + 1])[0] 

    def buff_uint8(self, offset):
        return unpack("b", self.buffer[offset:offset + 1])[0] 

    def buff_int16(self, offset):
        return unpack("h", self.buffer[offset:offset + 2])[0] 

    def buff_uint16(self, offset):
        return unpack("H", self.buffer[offset:offset + 2])[0] 

    def buff_int32(self, offset):
        return unpack("i", self.buffer[offset:offset + 4])[0] 

    def buff_uint32(self, offset):
        return unpack("I", self.buffer[offset:offset + 4])[0] 

    def buff_int64(self, offset):
        return unpack("q", self.buffer[offset:offset + 8])[0] 

    def buff_uint64(self, offset):
        return unpack("Q", self.buffer[offset:offset + 8])[0] 

    def buff_float(self, offset):
        return unpack("f", self.buffer[offset:offset + 4])[0] 

    def buff_double(self, offset):
        return unpack("d", self.buffer[offset:offset + 8])[0] 

    def buff_string(self, offset, length=16):
        result = unpack(f"{length}s", self.buffer[offset:offset+length])[0]
        if result[0] == b"\x00":
            return ""
        return result.split(b"\x00")[0].decode("utf-8")

    def buff_struct(self, offset, fmt):
        size = calcsize(fmt)
        return unpack(fmt, self.buffer[offset:offset+size])
    
    ## Regexp part ##
    def _get_min_max_addr_(self):
        """ Returns minimal and maximal address """
        class SYSTEM_INFO(Structure):
            _fields_ = [('wProcessorArchitecture', WORD),
                        ('wReserved', WORD),
                        ('dwPageSize', DWORD),
                        ('lpMinimumApplicationAddress', LPVOID),
                        ('lpMaximumApplicationAddress', LPVOID),
                        ('dwActiveProcessorMask', c_ulonglong if sizeof(c_void_p) == 8 else c_ulong), # pointer size depends on the OS verision  (32b or 64b)
                        ('dwNumberOfProcessors', DWORD),
                        ('dwProcessorType', DWORD),
                        ('dwAllocationGranularity', DWORD),
                        ('wProcessorLevel', WORD),
                        ('wProcessorRevision', WORD)]
        si = SYSTEM_INFO()
        is_64bit = False # TODO; however aok hd  is 32 bit anyway
        if is_64bit:
            windll.kernel32.GetNativeSystemInfo(byref(si))
            max_addr = si.lpMaximumApplicationAddress
        else:
            windll.kernel32.GetNativeSystemInfo(byref(si))
            max_addr = 2147418111
        min_addr = si.lpMinimumApplicationAddress
        return min_addr, max_addr

    def _VirtualQueryEx_(self, ptr):
        """ Returns filled memory basic informations about allocations """
        class MEMORY_BASIC_INFORMATION(Structure):
            _fields_ = [('BaseAddress', c_void_p),
                        ('AllocationBase', c_void_p),
                        ('AllocationProtect', DWORD),
                        ('RegionSize', c_size_t),
                        ('State', DWORD),
                        ('Protect', DWORD),
                        ('Type', DWORD)]
        # set arguments
        VirtualQueryEx = windll.kernel32.VirtualQueryEx
        VirtualQueryEx.argtypes = [HANDLE, LPCVOID, POINTER(MEMORY_BASIC_INFORMATION), c_size_t]
        VirtualQueryEx.restype = c_size_t
        # load
        mbi = MEMORY_BASIC_INFORMATION()
        if not VirtualQueryEx(self.process_handle, ptr, byref(mbi), sizeof(mbi)):
            print(f"Error VirtualQueryEx: {ptr}")
            raise
        return mbi

    def _iter_memory_region_(self):
        """ Loads memory region, generator
        Returns starting address and memory region size. 
        """
        min_address, max_address = self._get_min_max_addr_()
        offset = min_address
        #for offset, chunk_size in self.iter_region( protec=protec, optimizations=optimizations):
        while True:
            if offset >= max_address:
                break
            mbi = self._VirtualQueryEx_(offset)
            offset = mbi.BaseAddress
            chunk = mbi.RegionSize
            protect = mbi.Protect
            state = mbi.State
            if state & 0x12000: # memfree nad memresrrve
                offset += chunk
                continue
            if (not protect & 0x6) or protect & 0x700: # not readonly/rw page nocache, writecombine, guard
                offset += chunk
                continue
            yield offset, chunk
            offset += chunk
        
    def _get_chunk_(self, start, size):
        """ Returns the whole chunk """
        offset = start
        result = b""
        read = 0
        while read < size:
            try:
                # Calculate how much stuff will be loaded into the buffer
                if size - read <= PyMemory.BUFFER_SIZE:
                    self.buffer_load(offset + read, size - read)
                    result += self.buffer.raw[:size-read]
                    read += size-read
                    
                else:
                    self.buffer_load(offset + read, PyMemory.BUFFER_SIZE)
                    result += self.buffer.raw
                    read += PyMemory.BUFFER_SIZE
            except:
                return b""
        return result

    def re(self, regex): 
        """ Bruteforce search in memory 
        regex must be binary string 
        """
        if type(regex) != type(re.compile("")):
            regex = re.compile(regex, re.IGNORECASE)

        for offset, chunk in self._iter_memory_region_():
            stuff = self._get_chunk_(offset, chunk)
            for res in regex.finditer(stuff):
                yield res
        # Get the boundaries

    def update(self):
        self.memory_regions = [(start, start+length) for start, length in self._iter_memory_region_()]





pymemory = PyMemory()

if __name__ == '__main__':
    proc_name = "AoK HD.exe"
    print(f"Loading: {proc_name}")
    pymemory.load_process(proc_name)
    with pymemory as pm:
        print(f"PID: {pm.pid}")
        print(f"Base address: {hex(pm.base_address)}")
        result = pm.int32(pm.base_address)
        result = pm.struct(pm.base_address, "II")
        #result = pm.re(b"\[\d{1,4}\] Kova")
# EOF
