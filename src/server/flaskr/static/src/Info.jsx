import React from 'react';

export default class Info extends React.Component {
    render() {

        let infos = this.props.infos;

        return (
            <dl className="info">
                {Object.keys(infos).map(function(title) {
                    return (
                        <React.Fragment key={title}>
                        <dt>{title}</dt>
                        <dd>{infos[title]}</dd>
                        </React.Fragment>
                    )
                    }
                )}
            </dl>
        )
    }
}

