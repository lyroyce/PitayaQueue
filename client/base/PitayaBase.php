<?php
$GLOBALS['THRIFT_ROOT'] = __DIR__.'/../thrift';
require_once $GLOBALS['THRIFT_ROOT'].'/Protocol/TProtocol.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Protocol/TBinaryProtocol.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/TTransport.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/TSocket.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/TFramedTransport.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Exception/TException.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Exception/TTransportException.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Type/TType.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Type/TMessageType.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Factory/TStringFuncFactory.php';
require_once $GLOBALS['THRIFT_ROOT'].'/StringFunc/TStringFunc.php';
require_once $GLOBALS['THRIFT_ROOT'].'/StringFunc/Core.php';
require_once __DIR__.'/../pitaya/Types.php';
require_once __DIR__.'/../pitaya/Pitaya.php';

use Thrift\Protocol\TBinaryProtocol;
use Thrift\Transport\TSocket;
use Thrift\Transport\TFramedTransport;
use pitaya\PitayaClient;

class PitayaBase {

	protected $client;
	protected $transport;
	
	public function __construct($host, $port, $socketTimeout = 60000) {

		$this->socket = new TSocket($host, $port);
		if ($socketTimeout) {
			$this->socket->setRecvTimeout($socketTimeout);
		}
		$this->transport = new TFramedTransport($this->socket);
		$this->client = new PitayaClient(new TBinaryProtocol($this->transport));
	}
	public function connect() {
		try {
			$this->transport->open();		
			return true;
		} catch (Exception $e) {
			return false;
		}
	}
	public function disconnect() {
		$this->transport->close();
	}
}
