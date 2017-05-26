
var configuracao = null;
var gridCheques = null;

var gridColunas = [
	{ "visible": false },
	{ title: "N° Chq.", "width" : "45px" },
	{ title: "Favorecido" },
	{ title: "Data emissão", "width" : "45px" },
	{ title: "Empresa", "width" : "20%" },
	{ title: "Banco", "width" : "20%" },
	{ title: "Conta corrente" , "width" : "40px" },
	{ title: "Valor", "width" : "10%" }	
];

var gridLegendas = {
	"lengthMenu": "Mostrar _MENU_ cheques por página",
	"zeroRecords": "Vazia",
	"info": "Página _PAGE_ de _PAGES_",
	"search": "Pesquisar:",
	"infoEmpty": "Não há cheques para impressão",
	"infoFiltered": "(filtered from _MAX_ total records)",
	"paginate": {
		"first": "Primeira",
		"last": "Última",
		"next": "Avançar",
		"previous": "Voltar"
	}
};

var abrirConfiguracao = function() {
	if (!$("#token").val() || !$("#url-sienge").val()){
		$.notify.defaults({clickToHide: true, autoHide: false, autoHideDelay: 1000, elementPosition: 'bottom left'});
		$('#h-configuracao').notify("Acesse as configurações no Sienge em: Financeiro > Apoio > Caixa e Bancos > Configuração Integração appCheque", 'info');
	}
	$("#cheques-para-impressao").fadeOut(250, function () {
		$("#cheques-configuracao").fadeIn(250);
		$("#icone-cheque, #icone-ferramentas").removeClass("ativo");
		$("#icone-ferramentas").addClass("ativo");
		
		carregarConfiguracao();
	});
}
	
function carregarConfiguracao() {
	$("#url-sienge").val(configuracao['urlSienge']);
	$("#token").val(configuracao['token']);
	$("#porta-matricial").val(configuracao['matricial']['porta']);	
	$("#porta-matricial-outra").val(configuracao['matricial']['outra']);
	$("#porta-serial").val(configuracao['cheque']['porta']);
	$("#impressora-cheque").val(configuracao['cheque']['modelo']);
	$("#porta-serial-outra").val(configuracao['cheque']['outra']);
}

function existeConfiguracaoMatricial() {
	return $("#porta-matricial").val() != '';
}

function ehConfiguracaoMatricialValida() {
	return $("#porta-matricial").val() != 'OUTRA' || ($("#porta-matricial").val() == 'OUTRA' && $("#porta-matricial-outra").val() != '');
}

function existeConfiguracaoSerial() {
	return $("#impressora-cheque").val() != '' && $("#porta-serial").val() != '';
}

function ehConfiguracaoSerialValida() {
	return $("#porta-serial").val() != 'OUTRA'|| ($("#porta-serial").val() == 'OUTRA' && $("#porta-serial-outra").val() != '');
}

function validarConfiguracao() {
	$.notify.defaults({clickToHide: false, autoHide: true, autoHideDelay: 15000, elementPosition: 'bottom bottom'});
	if(existeConfiguracaoMatricial() && !ehConfiguracaoMatricialValida()) {
		mostrarMensagem({"status": "alerta","titulo": "Ops! Algo deu errado...", "mensagem":"Verifique as configurações da impressora matricial."});
		$('#porta-matricial-outra').notify("Configure a porta da impressora matricial.", 'warn');
		return;
	} 
	
	if(existeConfiguracaoSerial() && !ehConfiguracaoSerialValida()) {
		mostrarMensagem({"status": "alerta","titulo": "Ops! Algo deu errado...", "mensagem":"Verifique as configurações da impressora de cheque."});
		$('#porta-serial-outra').notify("Configure a porta da impressora de cheque.", 'warn');
		return;
	}

	if(!existeConfiguracaoSerial() && !existeConfiguracaoMatricial()) {
		mostrarMensagem({"status": "alerta","titulo": "Ops! Algo deu errado...", "mensagem":"É necessário configurar um tipo de impressora."});
		return;
	}
	
	configuracao['urlSienge'] = $("#url-sienge").val();
	configuracao['token'] = $("#token").val();
	configuracao['matricial']['porta'] = $("#porta-matricial").val();
	configuracao['matricial']['outra'] = $("#porta-matricial-outra").val();
	configuracao['cheque']['porta']= $("#porta-serial").val();
	configuracao['cheque']['modelo'] = $("#impressora-cheque").val();
	configuracao['cheque']['outra'] = $("#porta-serial-outra").val();
	
	salvarConfiguracao(configuracao, mostrarMensagem);
}

function main(ret) {
	this.configuracao = ret;
	
	if(!appConfigurado()) {		
		abrirConfiguracao();
	}
}

function appConfigurado() {
	return configuracao['urlSienge'] != '';
}

function verificarIconeSair() {
	if($(window).width() < 990) {			
		$("#btn-sair-sistema img").attr("src", "resources/imgs/sair-w.png");
	} else {
		$("#btn-sair-sistema img").attr("src", "resources/imgs/sair.png");
	}
}

function controleEsconderColunaEmpresa() {
	var column = gridCheques.column(4);
		
	if($(window).width() < 990) {			
		column.visible( false );
	} else {
		column.visible( true );
	}
}

$(document).ready(function(){
	buscarConfiguracao(main);
	carregarGridCheques();

	$('#grid-cheques tbody').on('click','tr', function () {
		$(this).toggleClass('selected');
		atualizaMensagemSelecao();
	});	
	
	$("#btn-sair-sistema").click(function() { 	
		sairApp();
	});
	
	$("#btn-icone-cheque").click(function() {
		if(!appConfigurado()) {
			mostrarMensagem({"status": "alerta","titulo": "Ops! Algo deu errado...", "mensagem":"Necessário configurar o aplicativo. Acesse os dados de conexão no Sienge: <br /><br /> <b>FINANCEIRO > APOIO > CAIXA E BANCOS > CONFIGURAÇÃO INTEGRAÇÃO APPCHEQUE</b>."});
			return;
		}
		
		$("#cheques-configuracao").fadeOut(250, function () {
			$("#cheques-para-impressao").fadeIn(250);
			$("#icone-cheque, #icone-ferramentas").removeClass("ativo");
			$("#icone-cheque").addClass("ativo");
		});
	});
	
	$("#btn-icone-ferramentas").click(abrirConfiguracao);
	$("#salvar-configuracao").click(validarConfiguracao);
	
	verificarIconeSair();
	controleEsconderColunaEmpresa();
	
	$("#btn-consultar-cheque").click(function() {   
			
		$("body").preloader("Buscando cheques...");
		
		$.getJSON("http://localhost:9151/" + gerarParametrosParaConsultaCheques() , function(data) { 			
			carregarGridCheques(data);        	
		}).error(function(data) {
		    console.log(data)
			mostrarMensagem(data['responseJSON']);
		}).complete(function() { 	
			$("body").removerPreloader();	
		});
		
	});

	$("#btn-imprimir-cheque").click(function() {
		if(quantidadeRegistrosSelecionados() != 0) {
			$("body").preloader("Imprimindo cheques...");
			$.post("http://localhost:9151/", gerarJsonParaImpressaoCheques("False", "False"), function(data) { 
				mostrarMensagem(data);
			}).error(function(data) {
		    	console.log(data);
				$("body").removerPreloader();
				mostrarMensagem(data['responseJSON']);
			}).complete(function() { 	
				$("body").removerPreloader();
				removeSelecaoCheques();
			});;
		} else {
			mostrarMensagem({"status": "alerta","titulo": "Ops! Algo deu errado...", "mensagem":"Selecione pelo menos um cheque para impressão."});
		}    
	});

	$("#btn-imprimir-copia").click(function() {
		if(quantidadeRegistrosSelecionados() != 0) {
			$("body").preloader("Imprimindo cópia do cheque...");
			$.post("http://localhost:9151/", gerarJsonParaImpressaoCheques("True", "False"), function(data) { 
				mostrarMensagem(data);
			}).error(function(data) {
		    	console.log(data);
				$("body").removerPreloader();
				mostrarMensagem(data['responseJSON']);
			}).complete(function() { 	
				$("body").removerPreloader();
			});;
		} else {
			mostrarMensagem({"status": "alerta","titulo": "Ops! Algo deu errado...", "mensagem":"Selecione pelo menos um cheque para impressão."});
		}    
	});

	$("#btn-imprimir-verso").click(function() {
		if(quantidadeRegistrosSelecionados() != 0) {
			$("body").preloader("Imprimindo verso do cheque...");
			$.post("http://localhost:9151/", gerarJsonParaImpressaoCheques("False", "True"), function(data) { 
				mostrarMensagem(data);
			}).error(function(data) {
		    	console.log(data);
				$("body").removerPreloader();
				mostrarMensagem(data['responseJSON']);
			}).complete(function() { 	
				$("body").removerPreloader();
			});;
		} else {
			mostrarMensagem({"status": "alerta","titulo": "Ops! Algo deu errado...", "mensagem":"Selecione pelo menos um cheque para impressão."});
		}
	});
	
	$(window).resize(function() {
		controleEsconderColunaEmpresa();
		verificarIconeSair();
	});

	$(window).on("beforeunload", function() { 
		sairApp();
	});

}); 


function gerarParametrosParaConsultaCheques() {
	var periodo = '';
	
	var dataInicio = $("#dataInicio").val();
	var dataFinal = $("#dataFinal").val();
	
	if(dataInicio) {
		periodo = dataInicio.replace('/', '-').replace('/', '-') + "/";
	}
	
	if(dataFinal) {
		periodo += dataFinal.replace('/', '-').replace('/', '-');
	}
	
	return periodo;
}

function gerarJsonParaImpressaoCheques(copia, verso) {
	var idPrinter = [];
	
	var getIdsRow = function(row, index) {		
		idPrinter[index] = row[0];
	}
	
	Array.from(gridCheques.rows('.selected').data()).forEach(getIdsRow);
	
    return "{ \"copia\" : \""+copia+"\", \"verso\" : \""+verso+"\", \"ids\" : [" + idPrinter + "] }";
}

function carregarGridCheques(cheques) {		
	if(gridCheques != null) {
		gridCheques.destroy();
	}

	gridCheques = $('#grid-cheques').DataTable({
		data: converterRetorno(cheques),
		columns: gridColunas,
		language: gridLegendas,
		ordering: false   
	});
}

function converterRetorno(ret) {
	if(ret == null) {		
		return '';       
	}
	cheques = [];	
	for (i = 0; i < ret.cheques.length; i++) {
		cheque = [];
		cheque[0] = ret.cheques[i].id;
		cheque[1] = ret.cheques[i].numeroCheque;
		cheque[2] = ret.cheques[i].nomeFavorecido;
		cheque[3] = ret.cheques[i].dataEmissao;
		cheque[4] = ret.cheques[i].codigoEmpresaView + ' - ' + ret.cheques[i].nomeEmpresa;
		cheque[5] = ret.cheques[i].codigoBanco + ' - ' + ret.cheques[i].nomeBanco;
		cheque[6] = ret.cheques[i].codigoContaCorrente;
		cheque[7] = ret.cheques[i].valor;
		cheques[i] = cheque;
	}	
	return cheques;	
}

function quantidadeRegistrosSelecionados() {
	return gridCheques.rows('.selected').data().length;
}

var msn;
function mostrarMensagem(jsonMensagem) {
	$("#hidden-content").find("h2").removeClass().addClass(jsonMensagem['status']).html(jsonMensagem['titulo'])
	$("#hidden-content").find("p").html(jsonMensagem['mensagem'])
	
	$("#mensagem").trigger("click");
}

function removeSelecaoCheques() {
	$("tr.selected").each(function(){
		$(this).toggleClass('printed');
		$(this).toggleClass('selected');
	});
	atualizaMensagemSelecao();
}

function atualizaMensagemSelecao(){
	var mensagem = '';		
	qtRegistrosSelecionados = quantidadeRegistrosSelecionados();		
	if(qtRegistrosSelecionados != 0) {
		mensagem =  '['+qtRegistrosSelecionados + ' cheque(s) selecionado(s) para impressão.]'; 
	}  		
	$("#grid-quantidade-cheques").html(mensagem);
}

