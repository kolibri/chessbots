import React from 'react';

export default class Moves extends React.Component {
    constructor(props) {
        super(props)
        this.clickHandler = this.clickHandler.bind(this);
        this.getSpanClassName = this.getSpanClassName.bind(this);
    }

    clickHandler(e) {
        this.props.onClickHandler(parseInt(e.target.dataset.index));
    }
    
    getSpanClassName(color, pair) {
        let classes = [
        color,
        this.props.currentMove === pair[color].index ? ' current' : ''
        ];

        return classes.join(' ');
    }

    render() {
        let moves = this.props.moves;
        let movePairs = [];


        for (let i=0; i < moves.length; i=i+2) {
            movePairs.push({ 
                w: {index: i, move: moves[i] }, 
                b: moves[i+1] ? {index: i+1, move: moves[i+1] }: null 
            });
        }

        return (
            <ol className="moves">
            {movePairs.map((pair, key) => 
                <li key={key}>
                <span 
                onClick={this.clickHandler} 
                data-index={pair.w.index}
                className={this.getSpanClassName('w', pair)}
                >
                {pair.w.move}
                </span>
                {pair.b !== null &&             
                    <span 
                    onClick={this.clickHandler} 
                    data-index={pair.b.index}
                    className={this.getSpanClassName('b', pair)}
                    >
                    {pair.b.move}
                    </span>
                }                    
                </li>)}
            </ol>
            )
    }
}

