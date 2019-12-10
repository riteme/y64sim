import React from 'react'
import { makeStyles } from '@material-ui/core/styles'
import MonacoEditor from 'react-monaco-editor'

import {
  Button,
  Select,
  MenuItem
} from '@material-ui/core'

const useStyles = makeStyles(theme => ({
  rootDiv: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%'
  },
  editorDiv: {
    flexGrow: 1,
    borderBottom: `1px solid ${theme.palette.divider}`
  },
  controlDiv: {
    display: 'flex'
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
  },
  compileButton: {
    borderRadius: 0
  }
}))

function CodeEditor({
  code, onCodeChange,
  language, onLanguageChange,
  classes
}) {
  const _classes = useStyles();

  const handleChange = event => {
    onLanguageChange(event.target.value);
  }

  return (
    <div className={[classes.root, _classes.rootDiv].join(" ")}>
      <div className={_classes.editorDiv}>
        <MonacoEditor
          value={code}
          onChange={onCodeChange}
        />
      </div>
      <div className={_classes.controlDiv}>
        <div className={_classes.controlLeft}>
          <div className={_classes.languageSelectDiv}>
            <Select value={language} onChange={handleChange} classes={{root: _classes.languageSelect}}>
              <MenuItem value="yo">.yo</MenuItem>
              <MenuItem value="ys">.ys</MenuItem>
            </Select>
          </div>
        </div>
        <div className={_classes.controlRight}>
          <Button
            color="primary"
            classes={{root: _classes.compileButton}}
          >COMPILE</Button>
        </div>
      </div>
    </div>
  )
}

export default CodeEditor;