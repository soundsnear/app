import * as dotenv from 'dotenv'
// @ts-ignore
dotenv.config('../.env')
// dotenv.config({ path: '../.env' })
import { Auth } from './spotify'
console.log('the url', Auth.getAuthUrl())