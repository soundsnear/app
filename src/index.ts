import * as dotenv from 'dotenv'
// @ts-ignore
dotenv.config('../.env')
// dotenv.config({ path: '../.env' })
import { Auth, spotifyApi } from './spotify'


const main = async () => {
  await Auth.setAccessAndRefreshTokensFromEnvironment()
  await Auth.refreshAccessToken()
  // const data = await spotifyApi.getArtistAlbums('43ZHCT0cAZBISjO8DG9PnE')
  // for (const album of data.body.items) {
  //   console.log(`album: ${album.name} tracks: ${album.total_tracks} images: ${album.images.map((image: any) => image.url)}`)
  // }

  const response = await spotifyApi.getMyDevices()
  const { devices } = response.body
  for (const device of devices) {
    console.log(device)
  }

  // todo; put this ito a function
  await spotifyApi.transferMyPlayback(['6321577cc2ebabba95365334fea411cbce39cd58'])
  https://open.spotify.com/album/3qnl7vvIjow4WCe2Bl9prX?si=10c56ffe026044e4

  await spotifyApi.addToQueue('spotify:track:0vFOzaXqZHahrZp6enQwQb')
  // await spotifyApi.addToQueue('spotify:track:0xzuKyeV52zNyjoAtRNMxD')
  // await spotifyApi.addToQueue('spotify:episode:73iBEaAYs24ttpbpg1PrZo')
  await spotifyApi.skipToNext()
  await spotifyApi.play()
}

main()