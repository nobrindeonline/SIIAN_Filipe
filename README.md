# SIIAN_Filipe

## Objetivo

Este desenvolvimento tem como objetivo organizar e centralizar a informação relativa a portes de envio, zonas geográficas, custos e prazos de entrega, permitindo posteriormente disponibilizar estes dados de forma estruturada através de SQL Server.

O ponto principal do trabalho foi criar uma estrutura que permitisse responder à necessidade de consultar:

- a zona geográfica aplicável;
- o prazo de entrega;
- o custo associado;
- e, sempre que possível, o critério que determina essa zona, como código postal, região ou província.

Para isso, foi criado um fluxo completo desde Excel até SQL Server, incluindo mecanismos de atualização e validação.

## Estrutura da solução

A solução foi organizada em duas componentes principais:

- ficheiros Excel, utilizados como fonte e manutenção dos dados;
- SQL Server, utilizado para armazenar e disponibilizar a informação através de tabelas e uma view.

