import argparse
import sys
class CustomArgParser(argparse.ArgumentParser):
    def error(self, message):
        print('error: %s\n' % message)
        self.print_help()
        sys.exit(-1)


class CommandLine:
    @classmethod
    def parse_args(cls) -> argparse.Namespace:
        parser = CustomArgParser(description="Ler código fonte para corrigir vulnerabilidades de segurança.\n\
Utilize o parâmetro api-server caso deseje iniciar o servidor REST.\n\n\
Exemplo para corrigir vulnerabilidades de segurança:\n\
  python src/app.py --entrypoint_folder=\"Wings\"\  --security_tool=\"42crunch\"\
--gen_fixes --overwrite_code_business_rules\n\n\
Exemplo para iniciar o servidor API REST:\n\
python src/app.py --api-server",
                                 formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("--api_server", dest="api_server", action="store_true",
                            help="Inicia API server, demais parâmetros são ignorados, deverão ser informados via chamada REST",
                            required=False)
        parser.add_argument("--entrypoint_folder", dest="entrypoint_folder", type=str,
                            help="Pasta que contém os arquivos a serem processados. Exemplo: Wings",
                            required=True)
        parser.add_argument("--security_tool", dest="security_tool", type=str,
                            help="Ferramenta de segurança a ser aplicada as correções. Ex: 42crunch",
                            required=False)
        parser.add_argument("--verbose", dest="verbose", action="store_true",
                            help="Se gera log das chamadas da IA. Default: false (opcional)",
                            required=False)
        args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

        return args
