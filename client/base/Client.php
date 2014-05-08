<?php
require_once 'PitayaBase.php';

class Client extends PitayaBase{
	public function queue($payload) {
		return $this->client->queue($payload);
	}
	public function query($jobId){
		return $this->client->query($jobId);
	}
}
