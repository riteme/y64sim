import React from 'react'
import { withStyles } from '@material-ui/core/styles'
import { withCookies } from 'react-cookie'

import {
  CssBaseline,
  Grid,
  Typography,
  Slider
} from '@material-ui/core'

import CodeIcon from '@material-ui/icons/Code'
import DashboardIcon from '@material-ui/icons/Dashboard'
import HelpIcon from '@material-ui/icons/Help'
import CheckCircleIcon from '@material-ui/icons/CheckCircle'
import CancelIcon from '@material-ui/icons/Cancel'
import MemoryIcon from '@material-ui/icons/Memory'
import SettingsIcon from '@material-ui/icons/Settings'

import ApplicationBar from './ApplicationBar'
import Pager from './Pager'
import CodeEditor from './CodeEditor'
import LoggingTerminal from './LoggingTerminal'
import PipelinePresentation from './PipelinePresentation'
import RegisterPage from './RegisterPage'
import MemoryPanel from './MemoryPanel'

const defaultBackend = 'http://localhost:5000/';

const styles = theme => ({
  main: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden'
  },
  container: {
    height: '100%'
  },
  page: {
    height: '100%',
    backgroundColor: theme.palette.common.white
  },
  applicationBarSpacer: theme.mixins.toolbar,
  pageLeft: {
    borderRight: `1px solid ${theme.palette.divider}`
  },
  pageRight: {
    display: 'flex',
    flexDirection: 'column',
    borderLeft: `1px solid ${theme.palette.divider}`
  },
  presentationDiv: {
    width: '100%',
    height: '100%',
    borderBottom: `1px solid ${theme.palette.divider}`
  },
  settings: {
    padding: theme.spacing(4)
  },
  heading: {
    padding: theme.spacing(0.5),
    color: theme.palette.grey[600],
    borderBottom: `1px solid ${theme.palette.divider}`
  },
  logInfo: {
    color: 'blue'
  },
  logDebug: {
    color: 'green'
  },
  logWarn: {
    color: 'orange'
  },
  logError: {
    color: 'red'
  }
})

class App extends React.Component {
  constructor(props) {
    super(props);

    this.UNKNOWN = <HelpIcon color="disabled" />;
    this.UPDATED = <CheckCircleIcon color="primary" />;
    this.FAILED = <CancelIcon color="error" />;

    this.DEFAULT_INTERVAL = 1000;

    this.state = {
      connected: false,
      backendUrl: defaultBackend,

      code: '',
      language: 'yo',
      diagnostics: [],

      frames: [],
      frameIndex: 0,

      errorStatusText: '',

      simulationInterval: this.DEFAULT_INTERVAL,
      simulateTimeoutHandle: null,
      playing: false,
      logging: [
        <span>Welcome to y64 Playground!</span>
      ],

      codeEditorDisableCompile: false,
      codeEditorStatus: this.UNKNOWN,
      codeEditorViewState: null,
      codeEditorQuerying: false
    }
  }

  componentDidMount() {
    this.checkConnection(this.state.backendUrl);
  }

  appendLogging(level, message) {
    const { classes } = this.props;
    const classMap = {
      'info': classes.logInfo,
      'debug': classes.logDebug,
      'warn': classes.logWarn,
      'error': classes.logError
    }
    this.setState(state => ({
      logging: state.logging.concat(
        <React.Fragment>
          <span className={classMap[level]}>({level}) </span>{message}
        </React.Fragment>
      )
    }))
  }

  checkConnection(url) {
    fetch(url)  // ping!
    .then(response => response.json())
    .then(result => {
      // console.log(result);

      if (result.status !== 'ok' || result.info !== 'pong')
        throw result;

      this.appendLogging('info', `Backend connected at "${this.state.backendUrl}"`)
      this.setState({
        connected: true
      })
    })
    .catch(() => {
      this.appendLogging('error', `Failed to connect to "${this.state.backendUrl}".`)
      this.setState({
        connected: false
      })
    });
  }

  invokeApi(api, body) {
    return fetch(new URL(api, this.state.backendUrl), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(body)
    });
  }

  async initializeFrame(bytes) {
    const response = await this.invokeApi('initialize', {
      memory_size: bytes.length,
      memory: bytes
    });
    console.debug(response);
    if (!response.ok) throw response;
    return response.json();
  }

  resolveParseResult = result => {
    console.debug(result);

    if (result.status === 'ok') {
      this.appendLogging('info', 'Source code compiled successfully.');
      this.setState({
        diagnostics: result.diagnostics,
        codeEditorStatus: this.UPDATED
      })

      this.initializeFrame(result.bytes)
      .then(result => {
        this.appendLogging('info', 'First frame loaded.')
        this.setState({
          frames: [result.frame],
          frameIndex: 0,
          playing: false
        })
      })
      .catch(r => {
        this.appendLogging('error', `Failed to initialize the first frame. ${r}`)
      });
    } else if ('diagnostics' in result) {
      this.appendLogging('error', 'Failed to compile source code.');
      this.setState({
        diagnostics: result.diagnostics,
        codeEditorStatus: this.FAILED
      })
    } else {
      this.appendLogging('error', 'Failed to compile source code.');
      this.setState({
        diagnostics: [{
          type: 'error',
          lineos: 0,
          code: '',
          message: `<backend>: backend failed: ${result.reason}`
        }],
        codeEditorStatus: this.FAILED
      })
    }
  }

  handleUrlChange = value => {
    try {
      this.checkConnection(new URL(value));
      this.setState({
        backendUrl: value
      })
    } catch {
      this.appendLogging('warn', `Invalid URL "${value}".`)
    }
  }

  handleCodeChange = value => {
    this.setState({
      code: value,
      codeEditorStatus: this.UNKNOWN
    })
  }

  handleLanguageChange = value => {
    this.setState({
      language: value
    })
  }

  handleSaveViewState = state => {
    this.setState({
      codeEditorViewState: state
    })
  }

  handleCompileAndLoad = () => {
    this.setState({
      codeEditorDisableCompile: true,
      codeEditorQuerying: true
    })

    this.invokeApi('parse', {
      type: this.state.language,
      content: this.state.code
    })
    .then(r => {
      this.setState({ codeEditorQuerying: false });
      if (!r.ok) throw r;
      return r.json();
    })
    .then(this.resolveParseResult)
    .catch(r => {
      console.debug(r);

      this.appendLogging('error', 'Failed to compile source code.');
      this.setState({
        codeEditorStatus: this.FAILED,
        diagnostics: [{
          'type': 'error',
          'lineos': 0,
          'code': '',
          'message': `<network>: failed to access parser: ${r.statusText} [HTTP ${r.status}] ${r}`
        }]
      })
    })
    .finally(() => {
      this.setState({
        codeEditorDisableCompile: false,
        codeEditorQuerying: false
      })
    })
  }

  async requestNextFrame() {
    try {
      const r = await this.invokeApi('simulate', {
        frame: this.state.frames[this.state.frames.length - 1]
      });

      console.debug(r);
      if (!r.ok) throw r;

      const result = await r.json();
      if (result.status === 'ok') {
        this.setState(state => ({
          frames: state.frames.concat(result.frame)
        }));

        for (const { level, message } of result.messages)
          this.appendLogging(level, `<server>: ${message}`);
      } else {
        this.appendLogging('error', result.reason);
      }

      return true;
    } catch (error) {
      console.debug(error);
      this.appendLogging('error', `Failed to fetch next frame.`);
      this.appendLogging('debug', `${error}`);

      if ('status' in error)
        this.appendLogging('debug', `${error.statusText} [HTTP ${error.status}]`);

      try {
        const json = await error.json();
        if ('status' in json)
          this.appendLogging('debug', `${json.status}: ${json.reason}`);
      } catch {}

      return false;
    }
  }

  setupFrame = frame => {
    if (frame.state !== 1) {
      const text = {
        0: 'UNKNOWN STATUS',
        2: 'INVALID INSTRUCTION',
        3: 'MEMORY ERROR',
        4: 'HALT DOWN',
        5: 'STALLED'
      }[frame.state];
      this.setState({
        errorStatusText: text
      });
    }
  }

  async simulateOneStep() {
    let index = this.state.frameIndex;
    let flag = true;
    if (index + 1 >= this.state.frames.length)
      flag = await this.requestNextFrame();

    if (flag) {
      index++;
      const frame = this.state.frames[index];
      this.setupFrame(frame);

      this.setState(state => ({
        frameIndex: state.frameIndex + 1
      }));
    }

    return flag;
  }

  prepareSimulation() {
    this.setState({
      playing: true,
      codeEditorDisableCompile: true
    });
  }

  pauseSimulation() {
    const handle = this.state.simulateTimeoutHandle;
    if (handle) clearTimeout(handle);

    this.setState({
      playing: false,
      codeEditorDisableCompile: false,
      simulateTimeoutHandle: null
    });
  }

  simulate = () => {
    if (this.getCurrentFrame().state !== 1) {
      this.pauseSimulation();
      this.appendLogging('warn', 'Simulation stopped due to processor error.')
    } else {
      this.simulateOneStep()
      .then(flag => {
        if (!flag) throw new Error('simulation failed');

        if (this.state.playing) {
          this.appendLogging('info', `[cycle = ${this.state.frameIndex}]`);

          const handle = setTimeout(this.simulate, this.state.simulationInterval);
          this.setState({
            simulateTimeoutHandle: handle
          });
        }
      })
      .catch(() => {
        this.appendLogging('error', 'An error occurred during execution.');
        this.pauseSimulation();
      });
    }
  }

  handleReset = () => {
    this.appendLogging('info', 'Reset to the first frame.');
    this.setState({
      frameIndex: 0
    })
  }

  handleStartPlay = () => {
    this.appendLogging('info', 'Start running program...');
    this.prepareSimulation();
    this.simulate();
  }

  handlePause = () => {
    this.appendLogging('info', 'Program execution paused.');
    this.pauseSimulation();
  }

  handleGoPrev = () => {
    this.appendLogging('info', `Navigate to previous frame. [cycle = ${this.state.frameIndex - 1}]`);
    this.setState(state => ({
      frameIndex: state.frameIndex > 0 ? state.frameIndex - 1 : 0
    }))
  }

  handleGoNext = () => {
    this.appendLogging('info', `Navigate to next frame. [cycle = ${this.state.frameIndex + 1}]`);
    this.simulateOneStep();
  }

  getCurrentFrame = () => {
    if (this.state.frames.length > 0)
      return this.state.frames[this.state.frameIndex];
    return null;
  }

  handleSetSimulationTimeInterval = (event, value) => {
    this.setState({
      simulationInterval: value
    })
  }

  render() {
    const { classes } = this.props;

    const frame = this.getCurrentFrame();
    let file = null;
    let cc = null;
    let rip = null;
    let state = null;
    let old_memory = null;
    let memory = null;
    if (frame !== null) {
      file = frame.registers;
      cc = frame.cc;
      rip = frame.rip;
      state = frame.state;
      memory = frame.memory;
      old_memory =
        this.state.frameIndex > 0 ?
        this.state.frames[this.state.frameIndex - 1].memory :
        null;
    }

    return (
      <React.Fragment>
        <CssBaseline />
        <div>
          <ApplicationBar
            connected={this.state.connected}
            defaultValue={defaultBackend}
            onUrlChange={this.handleUrlChange}
            currentBacked={this.state.backendUrl}
          />
          <main className={classes.main}>
            <div className={classes.applicationBarSpacer} />
            <Grid container spacing={0} className={classes.container}>
              <Grid item xs={6} className={[classes.page, classes.pageLeft].join(' ')}>
                <Pager
                  icons={[
                    <CodeIcon />,
                    <DashboardIcon />,
                    <MemoryIcon />,
                    <SettingsIcon />
                  ]}
                  pages={[
                    <React.Fragment>
                      <div className={classes.heading}>
                        <Typography variant="subtitle2">SOURCE</Typography>
                      </div>
                      <CodeEditor
                        code={this.state.code}

                        language={this.state.language}
                        disableCompile={this.state.codeEditorDisableCompile}
                        status={this.state.codeEditorStatus}
                        diagnostics={this.state.diagnostics}
                        viewState={this.state.codeEditorViewState}
                        querying={this.state.codeEditorQuerying}

                        onCodeChange={this.handleCodeChange}
                        onLanguageChange={this.handleLanguageChange}
                        onSaveViewState={this.handleSaveViewState}
                        onCompile={this.handleCompileAndLoad}
                      />
                    </React.Fragment>,
                    <React.Fragment>
                      <div className={classes.heading}>
                        <Typography variant="subtitle2">STATUS</Typography>
                      </div>
                      <RegisterPage
                        rip={rip}
                        state={state}
                        file={file}
                        cc={cc}
                      />
                    </React.Fragment>,
                    <React.Fragment>
                      <div className={classes.heading}>
                        <Typography variant="subtitle2">MEMORY</Typography>
                      </div>
                      <MemoryPanel
                        old={old_memory}
                        memory={memory}
                        rip={rip}
                      />
                    </React.Fragment>,
                    <React.Fragment>
                      <div className={classes.heading}>
                        <Typography variant="subtitle2">SETTINGS</Typography>
                      </div>
                      <div className={classes.settings}>
                        <Typography variant="subtitle1">
                          Simulation Step Interval
                        </Typography>
                        <Slider
                          defaultValue={this.DEFAULT_INTERVAL}
                          getAriaValueText={value => `${value}ms`}
                          value={this.state.simulationInterval}
                          valueLabelDisplay="auto"
                          step={50}
                          min={50}
                          max={5000}
                          marks={[
                            {value: 50, label: '50ms'},
                            {value: 1000, label: '1s'},
                            {value: 2000, label: '2s'},
                            {value: 3000, label: '3s'},
                            {value: 4000, label: '4s'},
                            {value: 5000, label: '5s'}
                          ]}
                          onChange={this.handleSetSimulationTimeInterval}
                        />
                      </div>
                    </React.Fragment>
                  ]}
                />
              </Grid>
              <Grid item xs={6} className={[classes.page, classes.pageRight].join(' ')}>
                <div className={classes.presentationDiv}>
                  <PipelinePresentation
                    enabled={this.state.frames.length > 0}
                    playing={this.state.playing}
                    frame={this.getCurrentFrame()}
                    frameIndex={this.state.frameIndex}
                    status={this.state.errorStatusText}

                    onReset={this.handleReset}
                    onStartPlay={this.handleStartPlay}
                    onPause={this.handlePause}
                    onGoPrev={this.handleGoPrev}
                    onGoNext={this.handleGoNext}
                  />
                </div>
                <div>
                  <LoggingTerminal
                    messages={this.state.logging}
                    height={280}
                  />
                </div>
              </Grid>
            </Grid>
          </main>
        </div>
      </React.Fragment>
    );
  }
}

export default withCookies(withStyles(styles)(App));