import * as React from "react";

export class List extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        let switches = this.props.items;
        const switchList = switches.map((s) =>
            <p>{s}</p>
        );

        return <div>{switchList}</div>;
    }
}
