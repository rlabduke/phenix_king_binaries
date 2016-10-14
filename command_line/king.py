# LIBTBX_SET_DISPATCHER_NAME phenix.king
import libtbx.load_env
from libtbx import easy_run
import os, sys, subprocess, platform, re

def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def run(args):
  #test for java on system
  which_java = which("java")
  if which_java is None:
    print "Java not detected on your system.  Please make sure java is in your path."
    sys.exit()

  #test java version
  java_version_out = easy_run.fully_buffered(command="java -version", join_stdout_stderr=True)
  java_version = None
  for line in java_version_out.stdout_lines:
    if line.startswith('java version'):
      java_version = line.split(" ")[2]
      if float(java_version[1:4]) < 1.5:
        print "KiNG requires java 1.5.0 or greater.  Please install a more recent java."
        sys.exit()

  #load main jars
  king_jar = libtbx.env.under_dist("king","king.jar")
  chiropraxis_jar = libtbx.env.under_dist("king","chiropraxis.jar")
  extratools_jar = libtbx.env.under_dist("king","extratools.jar")

  #determine JOGL version
  pf = platform.platform()
  if re.search("Darwin",pf):
    jogl_jar = libtbx.env.under_dist("king","macosx/jogl.jar")
    gluegen_jar = libtbx.env.under_dist("king","macosx/gluegen-rt.jar")
    jogl_path = libtbx.env.under_dist("king","macosx")
  elif re.search("Linux",pf):
    if re.search("x86_64",pf):
      jogl_jar = libtbx.env.under_dist("king","linux_amd64/jogl.jar")
      gluegen_jar = libtbx.env.under_dist("king","linux_amd64/gluegen-rt.jar")
      jogl_path = libtbx.env.under_dist("king","linux_amd64")
    else:
      jogl_jar = libtbx.env.under_dist("king","linux_i586/jogl.jar")
      gluegen_jar = libtbx.env.under_dist("king","linux_i586/gluegen-rt.jar")
      jogl_path = libtbx.env.under_dist("king","linux_i586")
  else:
    print "could not determine OS, not using openGL"
    jogl_jar = ""
    gluegen_jar = ""
    jogl_path = ""
  king_cmd = " ".join(["java",
                      "-Xms256m",
                      "-Xmx1024m",
                      "-cp",
                      king_jar+":"+extratools_jar+":"+chiropraxis_jar,
                      "king.KingMain"])
  args_str = " " + " ".join(args)
  king_job = easy_run.call(command=king_cmd + args_str)

if (__name__ == "__main__"):
  run(sys.argv[1:])
