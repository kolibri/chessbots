import React from 'react';
import Field from './Field.jsx';

export default class Board extends React.Component {
    render() {
        let fields = this.props.reverse ? 
            this.props.fields.reverse() : 
            this.props.fields;

        return (
            <div className="board">
            {fields.map((field) => 
                <Field 
                key={field.key} 
                piece={field.piece} 
                name={field.key} 
                move={this.props.move}
                selected={field.key === this.props.selected.key}
                clickHandler={this.props.clickHandler}
                />)}
            </div>
            )
    }
}
