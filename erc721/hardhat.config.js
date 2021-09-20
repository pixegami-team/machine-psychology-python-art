/**

* @type import('hardhat/config').HardhatUserConfig

*/

require("dotenv").config();
require("@nomiclabs/hardhat-ethers");

const { API_URL, PRIVATE_KEY, MAINNET_API_URL, MAINNET_PRIVATE_KEY } =
  process.env;

module.exports = {
  solidity: "0.8.0",
  defaultNetwork: "ropsten",
  networks: {
    hardhat: {},

    ropsten: {
      url: API_URL,
      accounts: [`0x${PRIVATE_KEY}`],
    },

    mainnet: {
      url: MAINNET_API_URL,
      accounts: [`0x${MAINNET_PRIVATE_KEY}`],
    },
  },
};
