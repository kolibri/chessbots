import './app.scss'
import React from 'react'
import ReactDOM from 'react-dom'
import Pgn from './src'


console.log('start')



document.addEventListener('DOMContentLoaded', function ()
{
    let games = document.querySelectorAll('.pgn').forEach(function(game, key){
        ReactDOM.render(
            <Pgn
                pgn = {game.innerHTML}
                player = {game.dataset.player}
                disableCustomMoves = {game.dataset.disableCustomMoves === "true"}
                reverse = {game.dataset.reverse === "true"}
                ply = {game.dataset.ply ? game.dataset.ply : null}
                pieceNames = {game.dataset.pieceNames ? JSON.parse(game.dataset.pieceNames) : null}
                key={key}
             />,
            game
        )
    });
})



console.log('end')
