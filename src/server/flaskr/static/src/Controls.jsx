import React from 'react';

export default class Moves extends React.Component {
    constructor(props) {
        super(props)
        this.moveHandler = this.moveHandler.bind(this);
        this.reverseHandler = this.reverseHandler.bind(this);
    }

    moveHandler(event) {
        event.preventDefault();
        let action = event.target.dataset.action;
        let moveIndex = 0;

        if ('back' === action) {
            moveIndex =  (this.props.ply > -1) ? this.props.ply - 1 : -1;
        }

        if ('next' === action) {
            moveIndex =  (this.props.ply < this.props.total - 1) ? this.props.ply + 1 : this.props.total -1;
        }
        if ('start' === action) {
            moveIndex = -1;
        }
        if ('end' === action) {
            moveIndex = this.props.total - 1;
        }
        
        this.props.gotoMoveHandler(moveIndex);
    }

    reverseHandler (event) {
        event.preventDefault();
        this.props.reverseHandler();
    }

    render() {
        return (
            <div>
            <button onClick={this.moveHandler} data-action="back">back</button>
            <button onClick={this.moveHandler} data-action="next">next</button>
            <button onClick={this.moveHandler} data-action="start">start</button>
            <button onClick={this.moveHandler} data-action="end">end</button>
            <button onClick={this.reverseHandler} data-action="turn">turn</button>
            </div>
        )
    }
}

