# backtv_django
Sistema de back-end da Smart TV

##Endpoints de acesso:

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/clima/ - temperatura

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/news/ - notícias

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/orgaos/ - lista de órgãos

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/orgaos/vistas/ - vistas abertas

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/orgaos/acervo/ - histórico do acervo

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/orgaos/detalhes/ - descrição do órgão

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/orgaos/acervo-classe/ - lista de acervo atual (por classe)

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/orgaos/financeiro/ - dados financeiros do órgão

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/orgaos/financeiro/agrupado/ - dados financeiros do órgão

http://devbacktv-devbacktv.devcloud.mprj.mp.br/api/membro/foto/ - Foto do servidor


## Endpoints para atualizar arquivos CSV's no Openshift
Os endpoints:

- api/orgaos/financeiro
- api/orgaos/financeiro/agrupado

Dependem de 3 arquivos CSV's:

- imoveis.csv
- orgaos.csv
- consolidacao.csv

Para criar/atualizar esses arquivos no Openshift, basta fazer uma requisição **PUT** para as seguintes URLS:

    HEADERS:
        Content-Type: application/csv
        Content-Disposition: attachment; filename=sheet.csv

    BODY:
        Respectivo arquivo csv

- imoveis: api/orgaos/upload/imoveis
- orgaos: api/orgaos/upload/orgaos
- consolidacao: api/orgaos/upload/consolidacao



endpoints internos a orgaos devem usar o parâmetro cdorg

endpoints internos a membro devem usar o parâmetro cdmat
