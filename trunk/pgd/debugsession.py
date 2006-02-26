import os
import sys

from winpdb import rpdb2
from console import Terminal

class SessionManagerInternal(rpdb2.CSessionManagerInternal):
    
    def _spawn_server(self, fchdir, ExpandedFilename, args, rid):
        """
        Start an OS console to act as server.
        What it does is to start rpdb again in a new console in server only mode.
        """

        #if g_fScreen:
        #    name = 'screen'
        #else:
        #    try:
        ##        import terminalcommand
        #        name = 'mac'
        #    except:
        #        name = os.name

        #if name == 'nt' and g_fDebug:
        #    name = 'nt_debug'
        
        #e = ['', ' --plaintext'][self.m_fAllowUnencrypted]
        #r = ['', ' --remote'][self.m_fRemote]
        #c = ['', ' --chdir'][fchdir]
        #p = ['', ' --pwd="%s"' % (self.m_pwd, )][os.name == 'nt']
        
        print self.m_pwd
        debugger = os.path.join(os.path.dirname(__file__), 'winpdb',
                   'rpdb2.py')
        if debugger[-1:] == 'c':
            debugger = debugger[:-1]

        #debug_prints = ['', ' --debug'][g_fDebug]    
        

        python_exec = sys.executable
        cmdargs = ['python', debugger,
                  '--debugee', '--chdir',# '--plaintext',
                  '--rid=%s' % rid, ExpandedFilename]
        #options = '"%s"%s --debugee%s%s%s%s --rid=%s "%s" %s' % (debugger, debug_prints, p, e, r, c, rid, ExpandedFilename, args)
        self.terminal.fork_command(python_exec, cmdargs)
        print 'forked', cmdargs
        

class SessionManager(rpdb2.CSessionManager):
    
    def __init__(self, app):
        self.app = app
        self.options = app.options
        self.main_window = app.main_window
        self.delegate = self._create_view()
        self._CSessionManager__smi = self._create_smi()

    def _create_smi(self):
        smi = SessionManagerInternal(
                                  self.options.pwd,
                                  self.options.allow_unencrypted,
                                  self.options.remote,
                                  self.options.host)
        smi.terminal = self
        return smi

    def _create_view(self):
        view = Terminal(self.app)
        self.main_window.attach_slave('outterm_holder', view)
        return view

    def fork_command(self, *args, **kw):
        self.delegate.terminal.fork_command(*args, **kw)

    def launch_filename(self, filename):
        self.app.launch(filename)
        
class RunningOptions(object):

    def set_options(self, command_line,
                  fAttach,
                  fchdir,
                  pwd,
                  fAllowUnencrypted,
                  fRemote,
                  host):
        self.command_line = command_line
        self.attach = fAttach
        self.pwd = pwd
        self.allow_unencrypted = fAllowUnencrypted
        self.remote = fRemote
        self.host = host


def connect_events(self):
    event_type_dict = {rpdb2.CEventState: {}}
    self.session_manager.register_callback(self.update_state, event_type_dict, fSingleUse = False)
    event_type_dict = {rpdb2.CEventStackFrameChange: {}}
    self.session_manager.register_callback(self.update_frame, event_type_dict, fSingleUse = False)
    event_type_dict = {rpdb2.CEventThreads: {}}
    self.session_manager.register_callback(self.update_threads, event_type_dict, fSingleUse = False)
    event_type_dict = {rpdb2.CEventNoThreads: {}}
    self.session_manager.register_callback(self.update_no_threads, event_type_dict, fSingleUse = False)
    event_type_dict = {rpdb2.CEventNamespace: {}}
    self.session_manager.register_callback(self.update_namespace, event_type_dict, fSingleUse = False)
    event_type_dict = {rpdb2.CEventThreadBroken: {}}
    self.session_manager.register_callback(self.update_thread_broken, event_type_dict, fSingleUse = False)
    event_type_dict = {rpdb2.CEventStack: {}}
    self.session_manager.register_callback(self.update_stack, event_type_dict, fSingleUse = False)
    event_type_dict = {rpdb2.CEventBreakpoint: {}}
    self.session_manager.register_callback(self.update_bp, event_type_dict, fSingleUse = False)


def start(command_line, fAttach, fchdir, pwd, fAllowUnencrypted, fRemote, host):
    options= RunningOptions()
    options.set_options(command_line, fAttach, fchdir, pwd, fAllowUnencrypted, fRemote, host)
    return options

def main(start):
    rpdb2.main(start)

def start_as_cl():
    rpdb2.main()

if __name__ == '__main__':
    start_as_cl()
