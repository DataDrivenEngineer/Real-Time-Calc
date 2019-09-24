(function() {
const socket = io('http://' + document.domain + ':' + location.port)
	//.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
  console.log('Websocket connected!');
});

/*socket.emit('connected', function() {
  console.log('Websocket connected!');
});*/

socket.on('json', function(responseJson) {
  console.log('Got response json. New equation string:' + responseJson.emitItem);
  app.$data.equationHistory.unshift(responseJson.emitItem);
	});

var app = new Vue({
    el: '#vmapp',
    data: {
      equation: '',
      result: 0,
      placeholder: 'Please type your equation...',
      equationHistory: [],
      equationString: ''
    },
    delimiters: ['[[',']]'],
    computed: {
      firstTen: function() {
        return this.equationHistory.slice(0, 10);
      }
    },
    
    created: function() {
      vm = this;
      //console.log('hi');
      socket.emit('initialization', {});
      socket.on('initial equations', function (responseJson) {
        console.log('initial eqs: ' + responseJson);
        vm.equationHistory = responseJson['equations'];
        //console.log(vm.equationHistory);
        //this.firstTen = this.equationHistory.slice(0, 10);
        //console.log(this.firstTen);
      });
    },
    
    methods: {
      
      /*eventListener: function() {
        var vm = this;
        socket.on('json', function(responseJson) {
          console.log('Got response json. New equation string:');
          vm.equationHistory.includes(responseJson.emitItem) ? {} : vm.equationHistory.unshift(responseJson.emitItem);
        });
      },*/

      calculate: function() {
        
        //connect to bus
        /*var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function() {
          console.log('Websocket connected!');
        });*/
        // checking if entered more than 1 operand
        var operands = [];
        var regex = /[\W]/g;
        var searchResults = [];
        var foundOperators = '';
        while ((searchResults = regex.exec(this.equation)) !== null) foundOperators += searchResults[0];
        if (foundOperators.length > 1) {
          alert('Nice try! Multiple operator support is yet to be added. Please stick to one operator for the time being...');
          this.equation = '';
          this.placeholder = 'Please type your equation...';
          return;
        }
        else if (this.equation.includes('/')) {
          operands = this.equation.split('/');
          result = (operands[0] / operands[1]).toString();
          equationString = `${operands[0]} / ${operands[1]} = ${result}`;
          this.equationHistory.unshift(equationString);
          socket.emit('json', {emitItem: equationString});
          console.log('Data emitted: ' + {emitItem: equationString});
          this.placeholder = result;
          this.equation = '';
          //return;
        }
        else if (this.equation.includes('*')) {
          operands = this.equation.split('*');
          result = (operands[0] * operands[1]).toString();
          equationString = `${operands[0]} * ${operands[1]} = ${result}`;
          this.equationHistory.unshift(equationString);
          socket.emit('json', {emitItem: equationString});
          console.log('Data emitted: ' + {emitItem: equationString});
          this.placeholder = result;
          this.equation = '';
          //return;
        }
        else if (this.equation.includes('-')) {
          operands = this.equation.split('-');
          result = (operands[0] - operands[1]).toString();
          equationString = `${operands[0]} - ${operands[1]} = ${result}`;
          this.equationHistory.unshift(equationString);
          socket.emit('json', {emitItem: equationString});
          console.log('Data emitted: ' + {emitItem: equationString});
          this.placeholder = result;
          this.equation = '';
          //return;
        }
        else if (this.equation.includes('+')) {
          operands = this.equation.split('+');
          result = (Number(operands[0]) + Number(operands[1])).toString();
          equationString = `${operands[0]} + ${operands[1]} = ${result}`;
          this.equationHistory.unshift(equationString);
          socket.emit('json', {emitItem: equationString});
          console.log('Data emitted: ' + {emitItem: equationString});
          this.placeholder = result;
          this.equation = '';
          //return;
        }
        //var vm = this;
        /*socket.on('json', function(responseJson) {
          console.log('Got response json. New equation string:');
          //console.log(responseJson);
          vm.equationHistory.includes(responseJson.emitItem) ? {} : vm.equationHistory.unshift(responseJson.emitItem);
          //vm.equationHistory.unshift(responseJson.emitItem);*/
        //});
      },
    },
      
      /*console.log('Preparing emission')
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function() {
          console.log('Websocket connected!');
        socket.emit('json', {someData: "Hello world!"});
        console.log('Data emitted');
        socket.on('json', function(responseJson) {
          console.log('Got response json:');
          console.log(responseJson);
        });
      });*/
  });
})()
