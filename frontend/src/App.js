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
import Presentation from './Presentation'
import Pager from './Pager'
import CodeEditor from './CodeEditor'
import PlaceholderPanel from './PlaceholderPanel'

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
  codeEditor: {
    borderRight: `1px solid ${theme.palette.divider}`
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
      bytes: [],
      diagnostics: [],

      codeEditorDisableCompile: false,
      codeEditorStatus: this.UNKNOWN,
      codeEditorViewState: null,
      codeEditorQuerying: false
    }
  }

  componentDidMount() {
    this.checkConnection(this.state.backendUrl);
  }

  checkConnection(url) {
    fetch(url)  // ping!
    .then(response => response.json())
    .then(result => {
      // console.log(result);

      if (result.status !== 'ok' || result.info !== 'pong')
        throw result;

      this.setState({
        connected: true
      })
    })
    .catch(() => {
      this.setState({
        connected: false
      })
    });
  }

  handleUrlChange = value => {
    this.checkConnection(value);
    this.setState({
      backendUrl: value
    })
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

  handleCompile = () => {
    this.setState({
      codeEditorDisableCompile: true,
      codeEditorQuerying: true
    })

    fetch(new URL('parse', this.state.backendUrl), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify({
        type: this.state.language,
        content: this.state.code
      })
    })
    .then(r => {
      this.setState({
        codeEditorQuerying: false
      })

      if (!r.ok) throw r;
      return r.json();
    })
    .then(result => {
      console.debug(result);

      if (result.status === 'ok') {
        this.setState({
          bytes: result.bytes,
          diagnostics: result.diagnostics,
          codeEditorStatus: this.UPDATED
        })
      } else if ('diagnostics' in result) {
        this.setState({
          diagnostics: result.diagnostics,
          codeEditorStatus: this.FAILED
        })
      } else {
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
    })
    .catch(r => {
      console.debug(r);

      this.setState({
        codeEditorStatus: this.FAILED,
        diagnostics: [{
          'type': 'error',
          'lineos': 0,
          'code': '',
          'message': `<network>: failed to access parser: ${r.statusText} (HTTP ${r.status})`
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
              <Grid item xs={6} className={classes.page}>
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
                      onCompile={this.handleCompile}

                      _classes={{root: classes.codeEditor}}
                    />,
                    <PlaceholderPanel />,
                    <PlaceholderPanel />,
                    <PlaceholderPanel />
                  ]}
                />
              </Grid>
              <Grid item xs={6} className={classes.page}>
                <PlaceholderPanel />
              </Grid>
            </Grid>
          </main>
        </div>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(App);