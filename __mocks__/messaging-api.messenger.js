// __mocks__/messaging-api-messenger.js
const jestMock = require('jest-mock');
const {
  Messenger,
  MessengerBatch,
  MessengerBroadcast,
  MessengerClient,
} = require.requireActual('messaging-api-messenger');
 
module.exports = {
  Messenger,
  MessengerBatch,
  MessengerBroadcast,
  MessengerClient: {
    connect: jest.fn(() => {
      const Mock = jestMock.generateFromMetadata(
        jestMock.getMetadata(MessengerClient)
      );
      return new Mock();
    }),
  },
};