class Pokebowl < Formula
  desc "Background runner for coding agents"
  homepage "https://github.com/TheLimeDev/PokeBowl"
  url "https://github.com/TheLimeDev/PokeBowl/releases/download/v0.1.1/pokebowl-0.1.1.tar.gz"
  sha256 "effe8f19500b441f7b73e2caf4eace55545a909fceed98cd143ecf7ab31ac7c5"
  version "0.1.1"
  depends_on "python@3.12"

  def install
    libexec.install Dir["*"]
    (bin/"pokebowl").write <<~EOS
      #!/bin/bash
      exec "#{Formula["python@3.12"].opt_bin}/python3" "#{libexec}/pokebowl.py" "$@"
    EOS
  end

  test do
    system "#{bin}/pokebowl", "--version"
  end
end
