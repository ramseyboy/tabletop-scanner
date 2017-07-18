import { combineReducers } from 'redux'
import {
    LOAD_SEARCH, SEARCH_COMPLETE
} from '../actions'

const searchResults = (state = {
    query: "",
    isFetching: false,
    results: []
}, action) => {
    switch (action.type) {
        case LOAD_SEARCH:
            return {
                ...state,
                isFetching: true,
                query: action.query,
                results : []
            };
        case SEARCH_COMPLETE:
            return {
                ...state,
                isFetching: false,
                query: action.query,
                results : action.results
            };
        default:
            return state
    }
};

const rootReducer = combineReducers({
    searchResults
});

export default rootReducer