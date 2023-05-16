const { PokemonShowdownClient } = require('pokemon-showdown');

// Create a new instance of the client
const client = new PokemonShowdownClient();

// Connect to the server
client.connect();
// When the client connects to the server
client.on('connect', () => {
    console.log('Connected to Pokemon Showdown server');
  
    // Find a battle room and join
    const room = client.joinRandomBattle();
  
    // Listen for battle events
    room.on('update', (args) => {
      // Handle battle updates
      console.log('Battle Update:', args);
    });
  
    room.on('chat', (args) => {
      // Handle chat messages in the battle
      console.log('Chat Message:', args);
    });
  
    // Send commands to the battle
    room.send('/choose move 1');
    room.send('/choose switch 2');
  });
  