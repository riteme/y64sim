import React from 'react'

import {
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListSubheader
} from '@material-ui/core'

import ErrorIcon from '@material-ui/icons/Error'
import WarningIcon from '@material-ui/icons/Warning'

function DiagnosticItem({
  diagnostic,
  onClick,
  index,
  value
}) {
  const handleClick = () => {
    onClick(diagnostic, index);
  }

  return (
    <ListItem
      onClick={handleClick}
      selected={index === value}
      button
    >
      <ListItemIcon>
        {diagnostic.type === 'error' ? <ErrorIcon color="error" /> : <WarningIcon htmlColor="orange" />}
      </ListItemIcon>
      <ListItemText
        primary={
          `[Line ${diagnostic.lineos}] ${diagnostic.message}`
        }
      />
    </ListItem>
  )
}

class DiagnosticPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      index: null
    }
  }

  dispatchResizeEvent() {
    window.dispatchEvent(new Event('resize'));  // notfiy monaco editor to resize
  }

  componentDidMount = this.dispatchResizeEvent;
  componentWillUnmount = this.dispatchResizeEvent;

  handleClick = (diagnostic, index) => {
    this.setState({
      index: index
    })
    this.props.onClickDiagnostic(diagnostic);
  }

  render() {
    const {
      diagnostics,
      classes
    } = this.props;

    let errorCount = 0;
    let warnCount = 0;
    for (let diag of diagnostics) {
      if (diag.type === 'error')
        errorCount++;
      else if (diag.type === 'warn')
        warnCount++;
    }

    return (
      <List
        component="nav"
        disablePadding
        dense
        subheader={
          <ListSubheader component="div" className={classes.header}>
            {errorCount} error{errorCount > 1 ? 's' : ''}, {warnCount} warning{warnCount > 1 ? 's' : ''}
          </ListSubheader>
        }
      >
        {diagnostics.map((data, index) =>
          <DiagnosticItem
            diagnostic={data}
            key={index}
            index={index}
            value={this.state.index}
            onClick={this.handleClick}
          />
        )}
      </List>
    )
  }
}

export default DiagnosticPanel;