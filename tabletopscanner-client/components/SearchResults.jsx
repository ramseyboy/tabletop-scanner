import * as React from "react";
import PropTypes from "prop-types";

export class SearchResults extends React.Component {

    static propTypes = {
        results: PropTypes.array.isRequired
    };

    static defaultProps = {
        results: []
    };

    render() {
        let results = this.props.results;
        const resultsList = results.map((r) =>
            <p key={r.geekid}>
                {r.name}
            </p>
        );

        return <div>{resultsList}</div>;
    }
}
