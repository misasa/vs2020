import logging
import psutil

class VS2020Process(object):
  exe_name = 'VisualStage.exe'
  pid = None

  @classmethod
  def is_running(cls):
    logging.debug('VS2020Process.is_running')
    if cls.pid == None:
      logging.debug('VS2020Process.pid is None')
      pid = cls.get_pid()
      return not pid == None
    else:
      logging.debug('VS2020Process.pid is %d' % cls.pid)
      return cls.check_pid(cls.pid)

  @classmethod
  def check_pid(cls, pid):
    logging.debug('VS2007Process.check_pid...')
    try:
      p = psutil.Process(pid)
      cnt = 0
      if p.name() == cls.exe_name:
        logging.debug('(%d) pid: %d [%s]' % (cnt, pid, cls.exe_name))
        return True
    except psutil.NoSuchProcess:
      logging.debug('NoSuchProcess')
      return False

  @classmethod
  def get_pid(cls):
    logging.debug('VS2020Process.get_pid...')
    if not cls.pid == None:
      return cls.pid
    cnt = 0
    for pid in psutil.pids():
      cnt += 1
      try:
        p = psutil.Process(pid)
        if p.name() == cls.exe_name:
          logging.debug('(%d) pid: %d [%s]' % (cnt, pid, cls.exe_name))
          cls.pid = pid
          return pid
      except psutil.NoSuchProcess:
        pass
      except psutil.AccessDenied:
        pass
