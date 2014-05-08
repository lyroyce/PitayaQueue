<?php
require_once 'PitayaBase.php';

abstract class Worker extends PitayaBase{

	public function __construct($host, $port){
		parent::__construct($host, $port);
		register_shutdown_function(array($this,'disconnect'));
	}
	public function take($timeout=10) {
		return $this->client->take($timeout);
	}
	public function done($jobId, $result=null){
		return $this->client->done($jobId, $result);
	}
	public function start(){
		$delay = 5;
		while(true){
			try{
				$this->connect();
				$job = $this->take();
				$this->disconnect();
				if($job->id!==null){
					$result = $this->work($job);
					$this->connect();
					$this->done($job->id, $result);	
					$this->disconnect();
				}
			}catch(\Exception $err){
				echo $err->getMessage().". Wait $delay seconds...\n";
				$this->disconnect();
				sleep($delay);
			}
		}
	}
	public abstract function work($job);
}
