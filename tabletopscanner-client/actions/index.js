import TabletopApi from '../services/TabletopApi.js';

export const LOAD_SEARCH = 'LOAD_SEARCH';
export const SEARCH_COMPLETE = 'SEARCH_COMPLETE';
// export const LOAD_SAVED = 'LOAD_SAVED';
// export const SAVED_COMPLETE = 'SAVED_COMPLETE';

export const loadSearch = query => ({
    type: LOAD_SEARCH,
    query
});

export const searchComplete = (query, json) => ({
    type: SEARCH_COMPLETE,
    query,
    results: json
});

export const search = query => (dispatch) => {
    dispatch(loadSearch(query));
    let api = new TabletopApi();
    return api.search(query)
        .then(resp => dispatch(searchComplete(query, resp.data)))
        .catch((error) => {
            console.log(error);
        })
};

// export const loadSaved = reddit => ({
//     type: LOAD_SAVED,
//     reddit
// });
//
// export const savedComplete = (saved, json) => ({
//     type: SAVED_COMPLETE,
//     saved,
//     posts: json.data.children.map(child => child.data),
//     receivedAt: Date.now()
// });
//
// const fetchSaved = reddit => dispatch => {
//     dispatch(requestSaved(reddit));
//     return fetch(`http://127.0.0.1:5000/api/search?q=scythe`)
//         .then(response => response.json())
//         .then(json => dispatch(receiveSaved(reddit, json)))
// };
//
// const shouldFetchSaved = (state, saved) => {
//     const savedGames = state.postsByReddit[saved];
//     if (!savedGames) {
//         return true
//     }
//     if (savedGames.isFetching) {
//         return false
//     }
//     return savedGames.didInvalidate
// };
//
// export const fetchSavedIfNeeded = saved => (dispatch, getState) => {
//     if (shouldPerformSearch(getState(), saved)) {
//         return dispatch(fetchPosts(saved))
//     }
// };
