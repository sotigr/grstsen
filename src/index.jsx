import React from 'react'
import ReactDOM from 'react-dom'

import Header from './components/Header/Header'
import Editor from './components/Editor/Editor'
import Ticker from './components/Ticker/Ticker'

import { usePythonApi } from './hooks/pythonBridge.js'


import './index.css'

const App = function() {
  return (
    <>
      <Header/>
      <Ticker/>
      <Editor/>
      <button   onClick={() => usePythonApi('select_file', "")}>
        open file
      </button>
    </>
  )
}

const view = App('pywebview')

const element = document.getElementById('app')
ReactDOM.render(view, element)