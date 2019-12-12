import React from 'react'
import { withStyles } from '@material-ui/core/styles'
import { ResponsiveMonacoEditor } from "responsive-react-monaco-editor"

import {
  Button,
  Select,
  MenuItem,
  LinearProgress,
  Fade
} from '@material-ui/core'

import DiagnosticPanel from './DiagnosticPanel'

const styles = theme => ({
  rootDiv: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    // height: '100%'
    flexGrow: 1
  },
  editorDiv: {
    flexGrow: 1,
    overflow: 'hidden',
  },
  controlDiv: {
    display: 'flex',
    borderTop: `1px solid ${theme.palette.divider}`
  },
  controlLeft: {
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(0.5),
    flexGrow: 1
  },
  languageSelectDiv: {
    marginLeft: theme.spacing(1)
  },
  languageSelect: {
    minWidth: 80
  },
  controlRight: {
    padding: theme.spacing(0.5),
    display: 'flex',
    flexDirection: 'row'
  },
  compileButton: {
    transition: [
      theme.transitions.create('color'),
      theme.transitions.create('background-color')
    ],
    borderRadius: 0
  },
  statusIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: [[0, theme.spacing(0.5), 0, theme.spacing(1)]]
  },
  diagnostics: {
    borderTop: `1px solid ${theme.palette.divider}`,
    overflow: 'auto',
    maxHeight: 250
  },
  diagnosticsHeader: {
    backgroundColor: theme.palette.background.paper,
    borderBottom: `1px solid ${theme.palette.divider}`
  }
})

class CodeEditor extends React.Component {
  constructor(props) {
    super(props);
    this.editor = null;
  }

  handleLanguageChange = event => {
    if (this.props.onLanguageChange)
      this.props.onLanguageChange(event.target.value);
  }

  editorDidMount = (editor, monaco) => {
    if (this.props.viewState)
      editor.restoreViewState(this.props.viewState);
    editor.focus();
    this.editor = editor;
    this.monaco = monaco;
  }

  handleClickDiagnostic = diagnostic => {
    console.debug(`navigate to ${diagnostic.lineos}`);
    this.editor.revealLine(diagnostic.lineos);
    this.editor.setPosition({
      lineNumber: diagnostic.lineos,
      column: 1
    });
    this.editor.focus();
  }

  highlightDiagnostics() {
    if (this.editor) {
      const model = this.editor.getModel();
      this.monaco.editor.setModelMarkers(model, 'y64sim', this.props.diagnostics.map(
        ({ lineos, type, message, code }) => ({
          code: code,
          message: message,
          startColumn: 1,
          endColumn: code.length + 1,
          startLineNumber: lineos,
          endLineNumber: lineos,
          severity: type === 'error' ?
            this.monaco.MarkerSeverity.Error :
            this.monaco.MarkerSeverity.Warning
        })
      ))
    }
  }

  componentDidUpdate() {
    this.highlightDiagnostics();
  }

  componentDidMount() {
    this.highlightDiagnostics();
  }

  componentWillUnmount() {
    if (this.props.onSaveViewState)
      this.props.onSaveViewState(this.editor.saveViewState());
  }

  render() {
    const {
      code, language,
      classes
    } = this.props;
    const monacoOptions = {
      minimap: {
        enabled: false
      },
      selectOnLineNumbers: true
    }

    return (
      <div className={classes.rootDiv}>
        <div className={classes.editorDiv} >
          <ResponsiveMonacoEditor
            value={code}
            onChange={this.props.onCodeChange}
            options={monacoOptions}
            editorDidMount={this.editorDidMount}
          />
        </div>
        {this.props.querying &&
        <Fade in>
          <LinearProgress variant="query" color="secondary" />
        </Fade>}
        {
          this.props.diagnostics.length > 0 &&
          (<Fade in>
            <div className={classes.diagnostics}>
              <DiagnosticPanel
                diagnostics={this.props.diagnostics}
                onClickDiagnostic={this.handleClickDiagnostic}
                classes={{header: classes.diagnosticsHeader}}
              />
            </div>
          </Fade>)
        }
        <div className={classes.controlDiv}>
          <div className={classes.controlLeft}>
            <div className={classes.languageSelectDiv}>
              <Select
                value={language}
                onChange={this.handleLanguageChange}
                classes={{root: classes.languageSelect}}
              >
                <MenuItem value="yo">.yo</MenuItem>
                <MenuItem value="ys">.ys</MenuItem>
              </Select>
            </div>
          </div>
          <div className={classes.controlRight}>
            <Button
              // variant="outlined"
              color="primary"
              onClick={this.props.onCompile}
              classes={{root: classes.compileButton}}
              disabled={this.props.disableCompile}
            >COMPILE & LOAD</Button>
            <div className={classes.statusIcon}>
              {this.props.status}
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default withStyles(styles)(CodeEditor);