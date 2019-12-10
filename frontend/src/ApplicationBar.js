import React from 'react'
import { fade, makeStyles } from '@material-ui/core/styles'

import {
  AppBar,
  Toolbar,
  Typography,
  InputBase
} from '@material-ui/core'

import WifiTetheringIcon from '@material-ui/icons/WifiTethering';
import PortableWifiOffIcon from '@material-ui/icons/PortableWifiOff';

const useStyles = makeStyles(theme => ({
  title: {
    flexGrow: 1
  },
  url: {
    position: 'relative'
  },
  status: {
    position: 'absolute',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    width: theme.spacing(6)
  },
  urlInput: {
    marginLeft: theme.spacing(6),
    padding: theme.spacing(1),
    color: theme.palette.common.white,
    transition: [
      theme.transitions.create('width'),
      theme.transitions.create('background-color')
    ],
    backgroundColor: fade(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: fade(theme.palette.common.white, 0.3)
    },
    width: 220,
    '&:focus': {
      width: 300
    }
  }
}))

// connected: connection icon
// onUrlChange: user typing
// defaultValue
function ApplicationBar(props) {
  const [state, setState] = React.useState({
    value: props.defaultValue,
    typingTimeoutHandle: 0
  })

  const handleChange = event => {
    if (state.typingTimeoutHandle) {
      clearTimeout(state.typingTimeoutHandle);
    }

    const url = event.target.value;
    setState({
      value: url,
      typingTimeoutHandle: setTimeout(() => {
        props.onUrlChange(url);
      }, 1000)
    });
  }

  const classes = useStyles();

  return (
    <AppBar position="fixed" elevation={0}>
      <Toolbar>
        <div className={classes.title}>
          <Typography variant="h6" noWrap>y64 Playground</Typography>
        </div>
        <div className={classes.url}>
          <div className={classes.status}>
            {props.connected ?
            <WifiTetheringIcon /> :
            <PortableWifiOffIcon color="error" />
            }
          </div>
          <InputBase
            classes={{input: classes.urlInput}}
            placeholder="Backend URL"
            defaultValue={props.defaultValue}
            onChange={handleChange}
          />
        </div>
      </Toolbar>
    </AppBar>
  );
}

export default ApplicationBar;