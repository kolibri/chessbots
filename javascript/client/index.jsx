require('../sass/style.scss');
import React from 'react'
import ReactDOM from 'react-dom'
import Client from './Client.jsx'

document.addEventListener('DOMContentLoaded', function ()
{
    console.log(document.getElementById('client'));
    ReactDOM.render(<Client />, document.getElementById('client'));
})
