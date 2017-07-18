import * as React from "react";
import PropTypes from "prop-types";
import {connect} from "react-redux";
import {search} from "../actions";
import styles from "./searchview.css";

class SearchView extends React.Component {

    static propTypes = {
        dispatch: PropTypes.func.isRequired
    };

    handleSearchSubmit = e => {
        if (e.charCode == 13) {
            let query = document.getElementById("search_input").value;
            this.props.dispatch(search(query))
        }
    };

    render() {
        return (
            <div className={styles.box}>
                <div className={styles.container}>
                    <input type="search" className={styles.search} id="search_input" placeholder="Search..."
                           onKeyPress={this.handleSearchSubmit}/>
                </div>
            </div>
        );
    };
}

export default connect()(SearchView)
