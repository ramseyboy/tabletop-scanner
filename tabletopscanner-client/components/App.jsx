import * as React from "react";
import PropTypes from "prop-types";
import {connect} from "react-redux";
import {SearchResults} from "../components/SearchResults";
import SearchView from "./SearchView"

class App extends React.Component {

    static propTypes = {
        results: PropTypes.array.isRequired,
        isFetching: PropTypes.bool.isRequired,
        dispatch: PropTypes.func.isRequired
    };

    static defaultProps = {
        results: [],
        isFetching: false
    };

    componentDidMount() {

    }

    componentWillReceiveProps(nextProps) {

    }

    render() {
        const {results, isFetching} = this.props;
        const isEmpty = !results || (results && results.length === 0);
        return (
            <div>
                {!isFetching && <SearchView />}
                <br/>
                {isEmpty
                    ? (isFetching ? <h2>Loading...</h2> : <h2>Empty.</h2>)
                    : <div style={{ opacity: isFetching ? 0.5 : 1 }}>
                    <SearchResults results={results}/>
                </div>
                }
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        results: state.searchResults.results,
        isFetching: state.searchResults.isFetching
    }
};

export default connect(mapStateToProps)(App)
