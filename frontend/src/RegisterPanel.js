import React from 'react'
import { makeStyles } from '@material-ui/core/styles'

import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Typography
} from '@material-ui/core'

import StatusText from './StatusText'
import { yellow } from '@material-ui/core/colors'

const useStyles = makeStyles(theme => ({
  root: {
    tableLayout: 'fixed',
    '& th:first-of-type': {
      borderRight: `1px solid ${theme.palette.divider}`
    }
  },
  names: {
    width: '25%'
  },
  span: {
    padding: [[0, theme.spacing(1)]]
  },
  highlight: {
    backgroundColor: yellow[300]
  },
  na: {
    color: theme.palette.text.hint,
    padding: [[theme.spacing(1), theme.spacing(3), theme.spacing(3)]]
  }
}))

function Cell({ left, right, highlight }) {
  const classes = useStyles();

  return (
    <React.Fragment>
      <TableCell align="right">
        <span className={[
          classes.span,
          highlight && classes.highlight
        ].join(' ')}>
          {left}
        </span>
      </TableCell>
      <TableCell align="right">
        <span className={[
          classes.span,
          highlight && classes.highlight
        ].join(' ')}>
          {right}
        </span>
      </TableCell>
    </React.Fragment>
  )
}

function RegisterValue({
  value,
  hex,
  translate,
  highlight
}) {
  return translate ?
  <Cell
    left={<StatusText state={parseInt(value)} />}
    right="(Not Available)"
    highlight={highlight}
  /> :
  <Cell
    left={value}
    right={hex === null ? '(Not Available)' : `0x${hex}`}
    highlight={highlight}
  />;
}

function RegisterPanel({
  data,
  old,
  translateState
}) {
  const classes = useStyles();

  if (data === null || data === undefined) return (
    <Typography variant="body1" className={classes.na}>Not Available</Typography>
  );

  let rows = []
  for (const key in data) {
    const [value, hex] = data[key];
    const highlight = old && key in old && value !== old[key][0];

    rows.push(
      <TableRow key={key}>
        <TableCell
          component="th"
          scope="row"
          align="center"
        >{key}</TableCell>
        <RegisterValue
          value={value}
          hex={hex}
          translate={translateState && key === 'state'}
          highlight={highlight}
        />
      </TableRow>
    )
  }

  return (
    <Table
      size="small"
      classes={{root: classes.root}}
    >
      <TableHead>
        <TableRow>
          <TableCell align="center" className={classes.names}>Name</TableCell>
          <TableCell align="right">Value</TableCell>
          <TableCell align="right">Hexadecimal</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {rows}
      </TableBody>
    </Table>
  )
}

export default RegisterPanel;