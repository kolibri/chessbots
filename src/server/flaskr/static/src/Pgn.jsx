import React from 'react';
import ChessjsAdapter from './ChessjsAdapter.js';
import Board from './Board.jsx';
import Info from './Info.jsx';
import Moves from './Moves.jsx';
import Controls from './Controls.jsx';

export default class Pgn extends React.Component {
    constructor(props) {
        super(props)
        this.adapter = new ChessjsAdapter(this.props.pgn);
        let moves = this.adapter.moves;
//         console.log(moves)
        this.state = {
            moves: moves,
            info: this.adapter.info(),
            ply: this.props.ply ? parseInt(this.props.ply) : moves.length - 1,
            reverse: this.props.reverse ? this.props.reverse : false,
            selected: {key: null}
        }

        this.gotoMove = this.gotoMove.bind(this);
        this.reverse = this.reverse.bind(this);
        this.clickField = this.clickField.bind(this);
    }

    formatMoves(moves){
        let pieceNames = this.props.pieceNames ? this.props.pieceNames : {'k': 'K', 'q': 'Q', 'b': 'B', 'n': 'N', 'r': 'R', 'p': ''}
        return this.adapter.translateMoves(pieceNames, moves);
    }

    gotoMove(moveIndex) {
        this.setState({ply: moveIndex});
    }

    reverse(){
        this.setState({reverse: !this.state.reverse});
    }

    clickField(fieldName){
        // stop on disables feature
        if (this.props.disableCustomMoves) {
            return;
        }
        let field = this.adapter.field(this.state.ply, fieldName);
        if (null === field) {
            return;
        }
        // no piece selected
        if (null === this.state.selected.key) {
            // no piece on this field
            if (null === field.piece) {
                return;
            }

            let playerToMove = (Math.abs(this.state.ply) % 2 == 1) ? 'w': 'b';
            // wrong player turn
            if (this.props.player && playerToMove !== this.props.player) {
                return;
            }

            // only allow, if current ply is last move 
            if (this.props.player && this.state.ply !== this.state.moves.length - 1){
                return;
            }

            // wrong piece color:
            if (playerToMove !== field.piece.color) {
                return;
            }

            // yeah, we can do something, set current field selected
            this.setState({selected: field});

            return;
        }

        // piece selected, so make move
        let newMoves = this.adapter.makeMove(this.state.ply, {
            from: this.state.selected.key,
            to: fieldName,
        });

        // invalid move, reset selected
        if (null == newMoves) {
            this.setState({ selected: { key: null }});
            return;
        }
        
        this.setState({
            moves: newMoves, 
            ply: this.state.ply+1,
            selected: {key: null}
        });
    }

    render() {
        return (
            <div>
            <Board 
                fields={this.adapter.fields(this.state.ply)} 
                move={this.adapter.getMove(this.state.ply)}
                reverse={this.state.reverse}
                selected={this.state.selected}
                clickHandler={this.clickField}
                key="board"/>
            <Controls 
                ply={this.state.ply} 
                total={this.state.moves.length} 
                gotoMoveHandler={this.gotoMove}
                reverseHandler={this.reverse}
                key="controls" />
            <Info infos={this.state.info} key="info"/>
            <Moves 
                moves={this.formatMoves(this.state.moves)} 
                onClickHandler={this.gotoMove}
                currentMove={this.state.ply}
                key="moves"/>
            </div>
            )
    }
}
