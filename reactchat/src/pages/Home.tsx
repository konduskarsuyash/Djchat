import React from 'react'
import { Box,CssBaseline } from '@mui/material'
import PrimaryAppBar from './template/PrimaryAppBar'
import PrimaryDraw from './template/PrimaryDraw'
import SecondaryDraw from './template/SecondaryDraw'

const Home = () => {

  return (
  <Box sx={{display:"flex"}}>
    <CssBaseline/>
    <PrimaryAppBar/>
    <PrimaryDraw></PrimaryDraw>
    <SecondaryDraw/>
  </Box>
  )
}

export default Home