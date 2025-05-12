document.getElementById('formulario').addEventListener('submit', function (event) {
    event.preventDefault();

    const octeto1 = parseInt(document.getElementById('octeto1').value);
    const octeto2 = parseInt(document.getElementById('octeto2').value);
    const octeto3 = parseInt(document.getElementById('octeto3').value);
    const octeto4 = parseInt(document.getElementById('octeto4').value);
    const mascara = parseInt(document.getElementById('mascara').value);

    const calcularEnderecos = (octetos, mascara) => {
        const ipDecimal = 
            (octetos[0] << 24) | 
            (octetos[1] << 16) | 
            (octetos[2] << 8) | 
            octetos[3];
        const maskBits = 32 - mascara;
        const subnetMask = ~((1 << maskBits) - 1);
        const networkAddress = ipDecimal & subnetMask;
        const broadcastAddress = networkAddress | ~subnetMask;

        const primeiroHost = mascara === 31 
            ? networkAddress 
            : networkAddress + 1;
        const ultimoHost = mascara === 31 
            ? broadcastAddress 
            : broadcastAddress - 1;

        const ipToString = (ip) => [
            (ip >> 24) & 255,
            (ip >> 16) & 255,
            (ip >> 8) & 255,
            ip & 255
        ].join('.');

        return {
            primeiroHost: ipToString(primeiroHost),
            ultimoHost: ipToString(ultimoHost),
            broadcast: ipToString(broadcastAddress),
            rede: ipToString(networkAddress)
        };
    };

    const calcularSubredesEHosts = (mascara) => {
        const bitsRede = mascara;
        const bitsHost = 32 - bitsRede;
        const numSubredes = Math.pow(2, bitsRede % 8) || 1;
        const numHosts = mascara === 31 ? 2 : Math.pow(2, bitsHost) - 2;
        return { numSubredes, numHosts };
    };

    const octetos = [octeto1, octeto2, octeto3, octeto4];
    const { primeiroHost, ultimoHost, broadcast, rede } = calcularEnderecos(octetos, mascara);
    const { numSubredes, numHosts } = calcularSubredesEHosts(mascara);

    let classeIp;
    if (octeto1 <= 127) classeIp = 'Classe A';
    else if (octeto1 <= 191) classeIp = 'Classe B';
    else if (octeto1 <= 223) classeIp = 'Classe C';
    else if (octeto1 <= 239) classeIp = 'Classe D';
    else classeIp = 'Classe E';

    const tipoRede = (octeto1 === 10 || (octeto1 === 192 && octeto2 === 168) || (octeto1 === 172 && octeto2 >= 16 && octeto2 <= 31)) 
        ? 'Rede privada' 
        : 'Rede pública';

    const tabela = document.getElementById('tabeladeresultados');
    tabela.innerHTML = `
        <tr><th colspan="2">Resultados</th></tr>
        <tr><td>Endereço IP:</td><td>${octeto1}.${octeto2}.${octeto3}.${octeto4}</td></tr>
        <tr><td>Máscara:</td><td>/${mascara}</td></tr>
        <tr><td>Endereço de Rede:</td><td>${rede}/${mascara}</td></tr>
        <tr><td>Primeiro host:</td><td>${primeiroHost}</td></tr>
        <tr><td>Último host:</td><td>${ultimoHost}</td></tr>
        <tr><td>Broadcast:</td><td>${broadcast}</td></tr>
        <tr><td>Classe:</td><td>${classeIp}</td></tr>
        <tr><td>Número de Sub-Redes:</td><td>${numSubredes}</td></tr>
        <tr><td>Hosts por Sub-Rede:</td><td>${numHosts}</td></tr>
        <tr><td>Endereço (Público/Privado):</td><td>${tipoRede}</td></tr>
    `;
});