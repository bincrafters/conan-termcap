import os
from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools


class TermcapConan(ConanFile):
    name = "termcap"
    version = "1.3.1"
    url = "https://github.com/bincrafters/conan-termcap"
    homepage = "https://www.gnu.org/software/termcap"
    description = "Enables programs to use display terminals in a terminal-independent manner"
    license = "GPL-2.0"
    topics = ("conan", "termcap", "terminal", "display")
    exports = ["LICENSE.md"]
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    _source_subfolder = "source_subfolder"
    _autotools = None

    def _unix_source(self):
        source_url = "https://ftp.gnu.org/gnu/termcap"
        sha256 = "91a0e22e5387ca4467b5bcb18edf1c51b930262fd466d5fda396dd9d26719100"
        tools.get("{}/termcap-{}.tar.gz".format(source_url, self.version), sha256=sha256)

    def _windows_source(self):
        source_url = "https://ufpr.dl.sourceforge.net/project/gnuwin32/termcap"
        sha256 = "fda35dfd5952b6b186040201b30d897c5c98bdc6d1865d12f53418b73770d308"
        tools.get("{}/{}/termcap-{}-src.zip".format(source_url, self.version, self.version), sha256=sha256)

    def source(self):
        self._windows_source()
        self._unix_source()

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def _configure_autotools(self):
        if not self._autotools:
            tools.replace_in_file("Makefile.in", "CFLAGS = -g", "")
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure()
            tools.replace_in_file("Makefile", "libtermcap.a info", "libtermcap.a")
        return self._autotools

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        source_path = "src" if self.settings.os == "Windows" else self.name + "-" + self.version
        os.rename(source_path, self._source_subfolder)
        if self.settings.compiler == "Visual Studio":
            cmake = self._configure_cmake()
            cmake.build()
        else:
            with tools.chdir(self._source_subfolder):
                autotools = self._configure_autotools()
                autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        if self.settings.compiler == "Visual Studio":
            cmake = self._configure_cmake()
            cmake.install()
        else:
            with tools.chdir(self._source_subfolder):
                autotools = self._configure_autotools()
                autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
