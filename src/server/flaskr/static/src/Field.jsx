import React from 'react';

export default class Field extends React.Component {
    constructor(props) {
        super(props)
        this.clickHandler = this.clickHandler.bind(this);
    }

    clickHandler (event) {
        event.preventDefault();
        this.props.clickHandler(event.target.dataset.name);
    }

    render() {
        let codeMap = {
            wk: '\u2654', wq: '\u2655', wr: '\u2656', wb: '\u2657', wn: '\u2658', wp: '\u2659', 
            bk: '\u265A', bq: '\u265B', br: '\u265C', bb: '\u265D', bn: '\u265E', bp: '\u265F'
        }
        let piece = piece 
        let pieceName = '';
        let pieceCode = '';
        
        if (this.props.piece) {
            pieceName = this.props.piece.color + this.props.piece.type;
            pieceCode = codeMap[pieceName] ? codeMap[pieceName] : '';
        }

        let classNames = [
            'field ',
            this.props.name,
            pieceName,
            (this.props.move ? (this.props.move.from === this.props.name ? ' from' : '') : ''),
            (this.props.move ? (this.props.move.to === this.props.name ? ' to' : '') : '' ),
            (this.props.selected ? ' selected' : '')
        ];

        let classes = classNames.join(' ');

        return (
            <div 
                className={classes} 
                data-name={this.props.name} 
                onClick={this.clickHandler}
                >{pieceCode}
            </div>
        )
    }
}

