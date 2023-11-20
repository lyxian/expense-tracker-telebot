from utils import updateSecretsEnv
import subprocess

class DB:
    def __init__(self, dbName=None, logFile=None):
        self.env = updateSecretsEnv()
        self.logFile = logFile
        self.dbName = dbName
        self.output = None
        self.cmd = None
        self.connString = ['mysql', '-h', self.env['DATABASE_HOST'], '-u', self.env['DATABASE_USER'], \
            '-p{}'.format(self.env['DATABASE_PASS']) , self.dbName, '-tvve']

        self.testConnection()

    def logOutput(self):
        with open(self.logFile, 'w') as f:
            if self.output:
                self.output = f'{self.output}'
            else:
                self.output = f'--- no output ---'
            f.write(self.output)
        self.output = None
        self.cmd = None

    def executeCommand(self):
        p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=self.env)
        self.output = p.stdout.read().decode().strip()
        self.logOutput()

    def testConnection(self):
        cmd = 'status'
        self.cmd = self.connString + [cmd]
        self.executeCommand()

    def runSelect(self, tableName, condition=None, count=None):
        if condition is None and count is None:
            cmd = f'SELECT * FROM {tableName};'
            self.cmd = self.connString + [cmd]
        else:
            pass
        self.executeCommand()

    # INSERT INTO Students(name, address, grades, phone) VALUES ('Harry', 'Potter', 31, 'USA');
    def runInsert(self, tableName, payload):
        if isinstance(payload, list):
            cmdStr = []
            for item in payload:
                newPayload = DB._formatPayload(item)
                cmdStr += [f'INSERT IGNORE INTO {tableName} ({newPayload[0]}) VALUES ({newPayload[1]});']
            cmd = '\n'.join(cmdStr)
        elif isinstance(payload, str):
            newPayload = DB._formatPayload(payload)
            cmd = f'INSERT INTO {tableName} ({newPayload[0]}) VALUES ({newPayload[1]});'
        else:
            raise Exception('invalid payload type')
        print(cmd)
        self.cmd = self.connString + [cmd]
        self.executeCommand()

    def runUpdate(self):
        self.executeCommand()

    def runDelete(self):
        self.executeCommand()

    @staticmethod
    def _formatPayload(payload):
        columns = []
        values = []
        for k, v in payload.items():
            columns += [k]
            if isinstance(v, int):
                values += [f'{v}']
            else:
                values += [f"'{v}'"]
        return ','.join(columns), ','.join(values)
