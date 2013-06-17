#!/usr/bin/python2
# Author: Alexandre Courbot <acourbot@nvidia.com>
# Latest source: https://github.com/Gnurou/logcatresolve
# This program can be distributed and modified without any constraint.
#
# This script filters adb logcat output and replaces native stack traces
# addresses and library files by the corresponding function name and 
# originating line in the source file.
#
# Usage;
# $ adb logcat |python logcatresolve.py
# The script needs some environment variables defined during Android build
# configuration in order to find the right library files. Therefore don't
# forget to run choosecombo or lunch with the same parameters as the build
# you are using.
import sys, re, subprocess, os, os.path

re = re.compile("#\\d+ +(pc +)([\\da-f]+) +([\/\\\.\\w]+)")
needed_env = ["ANDROID_PRODUCT_OUT", "ANDROID_EABI_TOOLCHAIN", "ANDROID_BUILD_TOP"]
addr2line_bin = ["arm-eabi-addr2line", "arm-linux-androideabi-addr2line"]
env = {}
addr2line_cmd = None

def addr2line(addr, shllib):
	return subprocess.check_output([addr2line_cmd, "-C", "-f", "-e", shllib, addr]).splitlines()

if __name__ == "__main__":
	for v in needed_env:
		env[v] = os.getenv(v)
		if not env[v]:
			print "Missing environment variable %s. Please configure Android for building."
			sys.exit(0)
	top = env["ANDROID_BUILD_TOP"]
	base = os.path.join(env["ANDROID_PRODUCT_OUT"], "symbols")
	for bin in addr2line_bin:
		tmp = os.path.join(env["ANDROID_EABI_TOOLCHAIN"], "arm-linux-androideabi-addr2line")
		if os.path.isfile(tmp):
			addr2line_bin = tmp
			break

	if not addr2line_bin:
		print("Cannot find addr2line binary!")
		sys.exit(1)

	for line in sys.stdin:
		m = re.search(line)
		if m:
			r = addr2line(m.group(2), os.path.join(base, m.group(3)[1:]))
			line = line[:m.start(1)] + r[0] + line[m.end(2):m.start(3)] + r[1][len(top) + 1:] + line[m.end(3):]
		sys.stdout.write(line)
		sys.stdout.flush()
