import React from 'react'
import { withStyles } from '@material-ui/core/styles'

import {
  CssBaseline,
  Grid
} from '@material-ui/core'

import CodeIcon from '@material-ui/icons/Code';
import VisibilityIcon from '@material-ui/icons/Visibility';

import ApplicationBar from './ApplicationBar'
import Presentation from './Presentation'
import Pager from './Pager'
import CodeEditor from './CodeEditor'

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

    this.state = {
      connected: false,
      backendUrl: defaultBackend,
      code: '',
      language: 'yo'
    }
  }

  componentDidMount() {
    this.checkConnection(this.state.backendUrl);
  }

  checkConnection(url) {
    fetch(url)  // ping!
    .then(response => response.json())
    .then(result => {
      console.log(result);

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
      code: value
    })
  }

  handleLanguageChange = value => {
    this.setState({
      language: value
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
                    <VisibilityIcon />
                  ]}
                  pages={[
                    <CodeEditor
                      code={this.state.code}
                      language={this.state.language}
                      onCodeChange={this.handleCodeChange}
                      onLanguageChange={this.handleLanguageChange}
                      classes={{root: classes.codeEditor}}
                    />,
                    <Presentation />
                  ]}
                />
              </Grid>
              <Grid item xs={6} className={classes.page}>
                <Presentation />
              </Grid>
            </Grid>
          </main>
        </div>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(App);