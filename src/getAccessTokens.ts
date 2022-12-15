import * as dotenv from 'dotenv'
// @ts-ignore
dotenv.config('../.env')
import { Auth } from "./spotify";

Auth.authorizeUsingCode()