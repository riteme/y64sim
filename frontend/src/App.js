import React from 'react'
import { withStyles } from '@material-ui/core/styles'

import {
  CssBaseline,
  Grid
} from '@material-ui/core'

import CodeIcon from '@material-ui/icons/Code'
import VisibilityIcon from '@material-ui/icons/Visibility'
import HelpIcon from '@material-ui/icons/Help'
import CheckCircleIcon from '@material-ui/icons/CheckCircle'
import CancelIcon from '@material-ui/icons/Cancel'
import BugReportIcon from '@material-ui/icons/BugReport'
import SettingsIcon from '@material-ui/icons/Settings'

import ApplicationBar from './ApplicationBar'
import Pager from './Pager'
import CodeEditor from './CodeEditor'
import PlaceholderPanel from './PlaceholderPanel'
import LoggingTerminal from './LoggingTerminal'
import PipelinePresentation from './PipelinePresentation'

const defaultBackend = 'http://localhost:5000/';

const styles = theme => ({
  main: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden'
  },
  container: {
    flexGrow: 1
  },
  page: {
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
    flexGrow: 1,
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

    this.state = {
      connected: false,
      backendUrl: defaultBackend,

      code: '',
      language: 'yo',
      diagnostics: [],

      frame: null,
      logging: [
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

  loadFrame(bytes) {
    this.invokeApi('initialize', {
      memory_size: bytes.length,
      memory: bytes
    })
    .then(r => {
      console.debug(r);
      if (!r.ok) throw r;
      return r.json();
    })
    .then(result => {
      this.appendLogging('info', 'First frame loaded.')
      this.setState({ frame: result.frame })
    })
    .catch(r => {
      this.appendLogging('error', `Failed to initialize the first frame. ${r}`)
    })
  }

  resolveParseResult = result => {
    console.debug(result);

    if (result.status === 'ok') {
      this.appendLogging('info', 'Source code compiled successfully.');
      this.setState({
        diagnostics: result.diagnostics,
        codeEditorStatus: this.UPDATED
      })

      this.loadFrame(result.bytes);
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
      const _ = new URL(value);
      this.checkConnection(value);
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

  render() {
    const { classes } = this.props;

    return (
      <React.Fragment>
        <CssBaseline />
        <div>
          <ApplicationBar
            connected={this.state.connected}
            defaultValue={defaultBackend}
            onUrlChange={this.handleUrlChange}
          />
          <main className={classes.main}>
            <div className={classes.applicationBarSpacer} />
            <Grid container spacing={0} className={classes.container}>
              <Grid item xs={6} className={[classes.page, classes.pageLeft].join(' ')}>
                <Pager
                  icons={[
                    <CodeIcon />,
                    <VisibilityIcon />,
                    <BugReportIcon />,
                    <SettingsIcon />
                  ]}
                  pages={[
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
                    />,
                    <PlaceholderPanel />,
                    <PlaceholderPanel />,
                    <PlaceholderPanel />
                  ]}
                />
              </Grid>
              <Grid item xs={6} className={[classes.page, classes.pageRight].join(' ')}>
                <div className={classes.presentationDiv}>
                  <PipelinePresentation />
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

export default withStyles(styles)(App);