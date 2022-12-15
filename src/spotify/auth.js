import SpotifyWebApi from 'spotify-web-api-node'

const clientId = process.env.SPOTIFY_CLIENT_ID
const clientSecret = process.env.SPOTIFY_CLIENT_SECRET
const redirectUri = 'https://example.com/callback'

const state = 'stateofwhat'

const scopes = [
  `app-remote-control`,
  `streaming`,
  `user-read-playback-state`,
  `user-modify-playback-state`,
  `user-read-currently-playing`,
]

const spotifyApi = new SpotifyWebApi({
  clientId,
  clientSecret,
  redirectUri,
});

export const authorizeUsingCode = async () => {
  const data = await spotifyApi.authorizationCodeGrant(process.env.SPOTIFY_CODE)
  console.log('The token expires in ' + data.body['expires_in']);
  console.log('The access token is ' + data.body['access_token']);
  console.log('The refresh token is ' + data.body['refresh_token']);
  // Set the access token on the API object to use it in later calls
  spotifyApi.setAccessToken(data.body['access_token']);
  spotifyApi.setRefreshToken(data.body['refresh_token']);
}

export const setAccessAndRefreshTokensFromEnvironment = () => {
  spotifyApi.setAccessToken(process.env.SPOTIFY_ACCESS_TOKEN);
  spotifyApi.setRefreshToken(process.env.SPOTIFY_REFRESH_TOKEN);
}

export const getAuthUrl = () => {
  const authorizeURL = spotifyApi.createAuthorizeURL(scopes, state)
  return authorizeURL
}

export {
  spotifyApi
}

export const refreshAccessToken = async () => {
  const response = await spotifyApi.refreshAccessToken()
  const accessToken = response.body.access_token
  spotifyApi.setAccessToken(accessToken)
}