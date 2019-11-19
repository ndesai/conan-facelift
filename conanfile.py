#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil

class FaceliftConan(ConanFile):
    name = "facelift"
    version = "1.0.0"
    description = "facelift"
    topics = ("conan", "facelift", "qface", "qt")
    url = "https://github.com/ndesai/conan-facelift"
    homepage = "https://github.com/Pelagicore/facelift"
    author = "Jacques Guillou <jacques.guillou@gmail.com>"
    license = "MIT"
    exports = ["LICENSE"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_qmlplugindump": [True, False],
        "enable_codegen": [True, False],
        "enable_dbus_ipc": [True, False],
        "force_disable_dbus_ipc": [True, False],
        "build_examples": [True, False],
        "build_tests": [True, False],
        "enable_desktop_dev_tools": [True, False],
        "disable_gtest": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "enable_qmlplugindump": False,
        "enable_codegen": False,
        "force_enable_dbus_ipc": False,
        "force_disable_dbus_ipc": False,
        "build_examples": True,
        "build_tests": False,
        "enable_desktop_dev_tools": False,
        "disable_gtest": False
    }
    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        git = tools.Git(folder=self.source_subfolder)
        git.clone("https://github.com/Pelagicore/facelift.git", "master")
        
    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["FACELIFT_ENABLE_QMLPLUGINDUMP"] = self.options.enable_qmlplugindump
        cmake.definitions["FACELIFT_ENABLE_CODEGEN"] = self.options.enable_codegen
        cmake.definitions["FACELIFT_ENABLE_DBUS_IPC"] = self.options.force_enable_dbus_ipc
        cmake.definitions["FACELIFT_DISABLE_DBUS_IPC"] = self.options.force_disable_dbus_ipc
        cmake.definitions["FACELIFT_BUILD_EXAMPLES"] = self.options.build_examples
        cmake.definitions["FACELIFT_BUILD_TESTS"] = self.options.build_tests
        cmake.definitions["FACELIFT_ENABLE_DESKTOP_DEV_TOOLS"] = self.options.enable_desktop_dev_tools
        cmake.definitions["FACELIFT_DISABLE_GTEST"] = self.options.disable_gtest

        if 'fPIC' in self.options and self.options.fPIC:
            cmake.definitions["CMAKE_C_FLAGS"] = "-fPIC"
            cmake.definitions["CMAKE_CXX_FLAGS"] = "-fPIC"
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        #self.copy(pattern="COPYING", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # if self.settings.os == "Windows" and not self.options.shared:
        #     self.cpp_info.libs.extend(['mswsock', 'ws2_32'])
        # elif self.settings.os == "Linux":
        #     self.cpp_info.libs.extend(['anl', 'pthread'])
        # elif self.settings.os == "QNX":
        #     self.cpp_info.libs.extend(['socket'])

