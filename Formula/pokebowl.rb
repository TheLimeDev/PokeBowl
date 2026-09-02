class Pokebowl < Formula
  desc "Background runner for coding agents"
  homepage "https://github.com/TheLimeDev/PokeBowl"
  url "https://github.com/TheLimeDev/PokeBowl/releases/download/v0.1.2/pokebowl-0.1.2.tar.gz"
  sha256 "fdca10762626373f494311c615d2007af6f4221fd29c1758eee5310fad6e8883"
  version "0.1.2"
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
