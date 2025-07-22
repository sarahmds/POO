import datetime
import enum

class Pagamento(enum.Enum):
    EmAberto = 1
    PagoParcial = 2
    Pago = 3

class Boleto:
    def _init__(self, cod: str, emissao: datetime.datetime, venc: datetime.datetime, valor: float):
        self._codBarras = cod
        self._dataEmissao = emissao
        self._dataVencimento = venc
        self._dataPago = None
        self._valorBoleto = valor
        self._valorPago = 0.0
        self._situacaoPagamento = Pagamento.EmAberto

    def Pagar(self, valorPago: float):
        if valorPago <= 0:
            raise ValueError("Valor de pagamento inválido.")
        self._valorPago += valorPago
        self._dataPago = datetime.datetime.now()
        self._situacaoPagamento = self.Situacao()

    def Situacao(self) -> Pagamento:
        if self._valorPago == 0:
            return Pagamento.EmAberto
        elif self._valorPago < self._valorBoleto:
            return Pagamento.PagoParcial
        else:
            return Pagamento.Pago

    def ToString(self) -> str:
        data_pago_str = self._dataPago.strftime("%d/%m/%Y %H:%M") if self._dataPago else "-"
        return (
            f"Código: {self._codBarras}\nEmissão: {self._dataEmissao}\nVencimento: {self._dataVencimento}\n"
            f"Valor: R${self._valorBoleto:.2f}\nPago: R${self._valorPago:.2f}\nData Pagamento: {data_pago_str}\n"
            f"Situação: {self._situacaoPagamento.name}"
        )


